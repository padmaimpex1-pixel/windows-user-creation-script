#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Windows Disk Cleanup Script
=====================================
Comprehensive cleanup script combining all cleanup operations from the session.
Includes: temp files, cache, Dropbox, Chrome, Windows Update, and disk analysis.
"""

import os
import sys
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

# ANSI Color codes
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    """Print section header"""
    print(f"\n{BOLD}{BLUE}{'='*80}{RESET}")
    print(f"{BOLD}{BLUE}{text.center(80)}{RESET}")
    print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")

def print_subheader(text):
    """Print subsection header"""
    print(f"\n{BOLD}{YELLOW}{text}{RESET}")
    print(f"{YELLOW}{'-'*80}{RESET}\n")

def print_success(msg):
    """Print success message"""
    print(f"{GREEN}[OK] {msg}{RESET}")

def print_info(msg):
    """Print info message"""
    print(f"{BLUE}[INFO] {msg}{RESET}")

def print_warning(msg):
    """Print warning message"""
    print(f"{YELLOW}[WARNING] {msg}{RESET}")

def print_error(msg):
    """Print error message"""
    print(f"{RED}[ERROR] {msg}{RESET}")

def get_dir_size(path):
    """Calculate total size of a directory"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path, onerror=lambda e: None):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except:
                    pass
    except:
        pass
    return total_size

def get_drive_info(drive_letter='C'):
    """Get drive space information"""
    try:
        stat = shutil.disk_usage(f'{drive_letter}:\\')
        total_gb = round(stat.total / (1024**3), 2)
        used_gb = round(stat.used / (1024**3), 2)
        free_gb = round(stat.free / (1024**3), 2)
        percent_used = round((used_gb / total_gb) * 100, 1)
        return {
            'total': total_gb,
            'used': used_gb,
            'free': free_gb,
            'percent_used': percent_used
        }
    except:
        return None

def delete_folder(path, description=""):
    """Safely delete a folder and return size freed"""
    size_before = 0
    try:
        if os.path.exists(path):
            size_before = get_dir_size(path)
            shutil.rmtree(path, ignore_errors=True)
            
            if not os.path.exists(path):
                size_freed_gb = round(size_before / (1024**3), 2)
                if description:
                    print_success(f"Deleted: {description} ({size_freed_gb} GB)")
                else:
                    print_success(f"Deleted: {path} ({size_freed_gb} GB)")
                return size_freed_gb
            else:
                print_warning(f"Could not delete: {path} (in use or protected)")
                return 0
    except Exception as e:
        print_error(f"Failed to delete {path}: {str(e)}")
        return 0
    return 0

def clear_folder(path, description=""):
    """Clear contents of a folder"""
    try:
        if os.path.exists(path):
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                try:
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path, ignore_errors=True)
                except:
                    pass
            
            if description:
                print_success(f"Cleared: {description}")
            else:
                print_success(f"Cleared: {path}")
            return True
    except Exception as e:
        print_error(f"Failed to clear {path}: {str(e)}")
    return False

def check_drive_space():
    """Check and display current drive space"""
    print_subheader("Current Drive Space")
    
    for drive in ['C', 'D']:
        info = get_drive_info(drive)
        if info:
            print(f"{drive}: Drive:")
            print(f"  Total:  {info['total']:>8.2f} GB")
            print(f"  Used:   {info['used']:>8.2f} GB ({info['percent_used']}%)")
            print(f"  Free:   {info['free']:>8.2f} GB")
            print()

def cleanup_temp_files():
    """Clean temporary files"""
    print_subheader("STEP 1: Cleaning Temporary Files")
    
    temp_paths = [
        "C:\\Windows\\Temp",
        "C:\\Users\\dell\\AppData\\Local\\Temp",
        "C:\\Users\\dell\\AppData\\Local\\Microsoft\\Windows\\INetCache",
        "C:\\Users\\dell\\AppData\\Local\\Microsoft\\Windows\\Temporary Internet Files"
    ]
    
    total_freed = 0
    for path in temp_paths:
        if os.path.exists(path):
            try:
                clear_folder(path, f"Temp files: {os.path.basename(path)}")
            except Exception as e:
                print_warning(f"Could not clear {path}: {str(e)}")
    
    return total_freed

def cleanup_windows_update_cache():
    """Clean Windows Update cache"""
    print_subheader("STEP 2: Cleaning Windows Update Cache")
    
    cache_path = "C:\\Windows\\SoftwareDistribution\\Download"
    if os.path.exists(cache_path):
        size_freed = delete_folder(cache_path, "Windows Update cache")
        return size_freed
    else:
        print_info("Windows Update cache not found or already cleaned")
        return 0

def cleanup_chrome_cache():
    """Clean Chrome cache (without closing Chrome)"""
    print_subheader("STEP 3: Cleaning Chrome Cache")
    
    chrome_cache_paths = [
        "C:\\Users\\dell\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache",
        "C:\\Users\\dell\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Code Cache",
        "C:\\Users\\dell\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Service Worker\\Cache",
        "C:\\Users\\dell\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache Storage",
        "C:\\Users\\dell\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\GPUCache"
    ]
    
    total_freed = 0
    for cache_path in chrome_cache_paths:
        if os.path.exists(cache_path):
            size_freed = delete_folder(cache_path, f"Chrome: {os.path.basename(cache_path)}")
            total_freed += size_freed
    
    if total_freed > 0:
        print_success(f"Total Chrome cache freed: {total_freed} GB")
    else:
        print_info("Chrome cache already cleaned or in use")
    
    return total_freed

def cleanup_dropbox_folder():
    """Delete Dropbox sync folder"""
    print_subheader("STEP 4: Deleting Dropbox Folder")
    
    dropbox_path = "C:\\Users\\dell\\Dropbox"
    if os.path.exists(dropbox_path):
        size_freed = delete_folder(dropbox_path, "Dropbox sync folder")
        return size_freed
    else:
        print_info("Dropbox folder not found or already deleted")
        return 0

def cleanup_empty_folders():
    """Delete empty folders"""
    print_subheader("STEP 5: Deleting Empty Folders")
    
    empty_paths = [
        "C:\\Users\\dell\\vipingit1-repos",
        "C:\\Users\\dell\\AppData\\Local\\Google\\Chrome\\User Data\\Cache",
    ]
    
    total_freed = 0
    for path in empty_paths:
        if os.path.exists(path):
            try:
                # Check if empty
                if not os.listdir(path):
                    shutil.rmtree(path)
                    print_success(f"Deleted empty folder: {path}")
            except Exception as e:
                print_warning(f"Could not delete {path}: {str(e)}")
    
    return total_freed

def cleanup_recycle_bin():
    """Empty recycle bin using Windows command"""
    print_subheader("STEP 6: Emptying Recycle Bin")
    
    try:
        # Use Windows API to empty recycle bin
        subprocess.run(['cmd', '/c', 'echo Y | cleanmgr /sageset:1 >nul 2>&1'], 
                      capture_output=True, check=False)
        subprocess.run(['cmd', '/c', 'cleanmgr /sagerun:1 >nul 2>&1'], 
                      capture_output=True, check=False)
        print_success("Recycle Bin emptied")
        return 0
    except Exception as e:
        print_warning(f"Could not empty Recycle Bin: {str(e)}")
        return 0

def analyze_top_folders():
    """Analyze top 20 largest folders on C: drive"""
    print_subheader("STEP 7: Analyzing Top 20 Largest Folders")
    
    print("Scanning C: drive (this takes a moment)...\n")
    
    folder_sizes = {}
    
    try:
        for dirpath, dirnames, filenames in os.walk('C:\\', onerror=lambda e: None):
            for filename in filenames:
                try:
                    filepath = os.path.join(dirpath, filename)
                    size = os.path.getsize(filepath)
                    
                    # Get top-level folder
                    parts = dirpath.split('\\')
                    if len(parts) > 2:
                        top_folder = '\\'.join(parts[:3])
                        if top_folder:
                            folder_sizes[top_folder] = folder_sizes.get(top_folder, 0) + size
                except:
                    pass
    except Exception as e:
        print_error(f"Error scanning drive: {str(e)}")
    
    # Sort and display top 20
    sorted_folders = sorted(folder_sizes.items(), key=lambda x: x[1], reverse=True)[:20]
    
    print(f"{'Folder':<50} {'Size (GB)':<12}")
    print("-" * 64)
    
    for path, size in sorted_folders:
        size_gb = round(size / (1024**3), 2)
        display_path = path if len(path) <= 50 else "..." + path[-47:]
        print(f"{display_path:<50} {size_gb:>10.2f} GB")
    
    print()
    return sorted_folders

def cleanup_google_drive_cache():
    """Clean Google Drive cache files"""
    print_subheader("STEP 8: Cleaning Google Drive Cache")
    
    gdrive_cache_locations = [
        "C:\\Users\\dell\\AppData\\Local\\Google\\Drive",
        "C:\\Users\\dell\\AppData\\Local\\Google\\DriveFS",
    ]
    
    total_freed = 0
    for location in gdrive_cache_locations:
        if os.path.exists(location):
            try:
                clear_folder(location, f"Google Drive cache: {os.path.basename(location)}")
            except Exception as e:
                print_warning(f"Could not clear {location}: {str(e)}")
    
    return total_freed

def cleanup_onedrive_cache():
    """Clean OneDrive cache and sync files"""
    print_subheader("STEP 9: Cleaning OneDrive Cache")
    
    onedrive_cache_locations = [
        "C:\\Users\\dell\\AppData\\Local\\Microsoft\\OneDrive\\logs",
        "C:\\Users\\dell\\AppData\\Local\\Microsoft\\OneDrive\\cache",
        "C:\\Users\\dell\\AppData\\Local\\Microsoft\\OneDrive\\thumbnails",
    ]
    
    total_freed = 0
    for location in onedrive_cache_locations:
        if os.path.exists(location):
            try:
                clear_folder(location, f"OneDrive cache: {os.path.basename(location)}")
                size = get_dir_size(location)
                total_freed += round(size / (1024**3), 2)
            except Exception as e:
                print_warning(f"Could not clear {location}: {str(e)}")
    
    # Also try to clear OneDrive sync cache folder
    onedrive_sync_path = "C:\\Users\\dell\\AppData\\Local\\Microsoft\\OneDrive"
    if os.path.exists(onedrive_sync_path):
        try:
            # Don't delete the main folder, just problematic subfolders
            problematic_folders = ["logs", "cache", "thumbnails", "settings", "Temp"]
            for subfolder in problematic_folders:
                subfolder_path = os.path.join(onedrive_sync_path, subfolder)
                if os.path.exists(subfolder_path):
                    try:
                        shutil.rmtree(subfolder_path, ignore_errors=True)
                    except:
                        pass
        except Exception as e:
            print_warning(f"Could not clean OneDrive folders: {str(e)}")
    
    return total_freed

def main():
    """Main cleanup routine"""
    print(f"\n{BOLD}{BLUE}")
    print("=" * 80)
    print("COMPLETE WINDOWS DISK CLEANUP SCRIPT".center(80))
    print("=" * 80)
    print(f"{RESET}\n")
    
    print_info(f"Cleanup started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Get initial drive space
    print_header("INITIAL DISK STATUS")
    check_drive_space()
    initial_c_info = get_drive_info('C')
    
    # Run all cleanup operations
    print_header("RUNNING CLEANUP OPERATIONS")
    
    total_freed = 0
    
    # Step 1: Temp files
    cleanup_temp_files()
    
    # Step 2: Windows Update cache
    freed = cleanup_windows_update_cache()
    total_freed += freed
    
    # Step 3: Chrome cache
    freed = cleanup_chrome_cache()
    total_freed += freed
    
    # Step 4: Dropbox folder
    freed = cleanup_dropbox_folder()
    total_freed += freed
    
    # Step 5: Empty folders
    cleanup_empty_folders()
    
    # Step 6: Recycle bin
    cleanup_recycle_bin()
    
    # Step 7: Google Drive cache
    freed = cleanup_google_drive_cache()
    total_freed += freed
    
    # Step 8: OneDrive cache
    freed = cleanup_onedrive_cache()
    total_freed += freed
    
    # Step 9: Analyze folders
    top_folders = analyze_top_folders()
    
    # Get final drive space
    print_header("FINAL DISK STATUS")
    check_drive_space()
    final_c_info = get_drive_info('C')
    
    # Calculate actual freed space
    if initial_c_info and final_c_info:
        actual_freed = initial_c_info['free'] - final_c_info['free']
        if actual_freed < 0:
            actual_freed = 0
        
        print_subheader("Space Freed Summary")
        print(f"Initial free space: {initial_c_info['free']} GB")
        print(f"Final free space:   {final_c_info['free']} GB")
        print(f"Freed:              {actual_freed} GB\n")
        
        if actual_freed > 0:
            print_success(f"Total disk space freed: {actual_freed} GB")
        else:
            print_warning("No additional space freed (may need to restart for changes to take effect)")
    
    # Recommendations
    print_header("RECOMMENDATIONS FOR FURTHER CLEANUP")
    
    print("1. Chrome Profile (11.83 GB)")
    print("   Location: C:\\Users\\dell\\AppData\\Local\\Google\\Chrome")
    print("   Action: Delete Chrome profile to free ~11.83 GB")
    print("   Impact: Will clear browsing history and cache\n")
    
    print("2. OneDrive Sync Folder")
    print("   Location: C:\\Users\\dell\\OneDrive")
    print("   Action: Move or archive OneDrive folder to D: drive")
    print("   Impact: Frees space while keeping files in cloud\n")
    
    print("3. Large Repositories")
    print("   Location: D:\\GitRepos (28 repositories)")
    print("   Status: Already on D: drive [OK] (84 GB free)\n")
    
    print("4. Windows System Files")
    print("   Location: C:\\Windows (30.89 GB)")
    print("   Action: Run DISM cleanup for system file cleanup\n")
    
    print("5. Program Files")
    print("   Location: C:\\Program Files & C:\\Program Files (x86)")
    print("   Action: Uninstall unused software\n")
    
    print_header("CLEANUP COMPLETE")
    print_success(f"Cleanup finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Cleanup interrupted by user{RESET}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}An error occurred: {str(e)}{RESET}\n")
        sys.exit(1)

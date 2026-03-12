#!/usr/bin/env python3
"""
Git Commit History Generator - Custom Date Range Version
Generates commits for a custom 2-year period with random distribution.
"""

import os
import sys
import subprocess
import random
from datetime import datetime, timedelta

def run_command(cmd, env=None):
    """Execute a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            env=env
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_git_initialized():
    """Check if current directory is a git repository."""
    success, _, _ = run_command("git rev-parse --git-dir")
    return success

def check_uncommitted_changes():
    """Check if there are any uncommitted changes in the repository."""
    success, stdout, _ = run_command("git status --porcelain")
    if not success:
        return False
    return len(stdout.strip()) == 0

def generate_random_commit_date(date):
    """Generate a random time for the given date."""
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    random_time = date.replace(hour=hour, minute=minute, second=second)
    return random_time.isoformat()

def create_commit(commit_date, commit_count):
    """Create a single git commit with custom date."""
    try:
        with open("activity_log.txt", "a") as f:
            timestamp = commit_date.isoformat()
            f.write(f"Commit #{commit_count}: {timestamp}\n")
        
        success, _, _ = run_command("git add activity_log.txt")
        if not success:
            return False
        
        iso_date = commit_date.isoformat()
        commit_message = f"Auto-generated commit #{commit_count}"
        
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = iso_date
        env["GIT_COMMITTER_DATE"] = iso_date
        
        cmd = f'git commit -m "{commit_message}"'
        success, _, _ = run_command(cmd, env=env)
        
        return success
        
    except Exception:
        return False

def generate_commit_history(start_year=2022, start_month=3, end_year=2023, end_month=3):
    """
    Generate commit history for custom date range.
    
    Args:
        start_year: Starting year (e.g., 2022)
        start_month: Starting month (e.g., 3 for March)
        end_year: Ending year (e.g., 2023)
        end_month: Ending month (e.g., 3 for March)
    """
    print("=" * 60)
    print("Git Commit History Generator (2022-2023)")
    print("=" * 60)
    
    # Pre-flight checks
    print("\n[1/5] Running pre-flight checks...")
    
    if not check_git_initialized():
        print("✗ Not a git repository.")
        sys.exit(1)
    print("✓ Git repository detected")
    
    if not check_uncommitted_changes():
        print("✗ Uncommitted changes detected.")
        sys.exit(1)
    print("✓ No uncommitted changes")
    
    # Create date range
    print("\n[2/5] Generating commit schedule...")
    start_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1)
    
    total_commits = 0
    commits_per_day = {}
    
    current_date = start_date
    while current_date <= end_date:
        num_commits = random.randint(2, 5)
        commits_per_day[current_date.date()] = num_commits
        total_commits += num_commits
        current_date += timedelta(days=1)
    
    days = (end_date - start_date).days
    print(f"✓ Scheduled {total_commits} commits across {days} days")
    print(f"  Period: {start_date.date()} to {end_date.date()}")
    print(f"  Average commits per day: {total_commits / max(days, 1):.2f}")
    
    # Create commits
    print("\n[3/5] Creating commits (this may take a while)...")
    commit_count = 0
    failed_count = 0
    
    current_date = start_date
    while current_date <= end_date:
        num_commits = commits_per_day[current_date.date()]
        
        for i in range(num_commits):
            random_time = generate_random_commit_date(current_date)
            commit_datetime = datetime.fromisoformat(random_time)
            
            if create_commit(commit_datetime, commit_count + 1):
                commit_count += 1
                if commit_count % 100 == 0:
                    print(f"  Created {commit_count} commits...")
            else:
                failed_count += 1
        
        current_date += timedelta(days=1)
    
    # Summary
    print("\n[4/5] Generation complete!")
    print("=" * 60)
    print(f"✓ Successfully created: {commit_count} commits")
    if failed_count > 0:
        print(f"✗ Failed commits: {failed_count}")
    print("=" * 60)
    
    print("\nNEXT STEPS:")
    print("1. View commits: git log --oneline | head -20")
    print("2. Push to GitHub: git push origin main --force")
    print("=" * 60)

def main():
    """Main entry point."""
    try:
        if not check_git_initialized():
            print("Error: Not a git repository")
            sys.exit(1)
        
        print("Generating 2022-2023 commit history...\n")
        # Generate from March 2022 to March 2023 (1 year = ~730 days)
        generate_commit_history(start_year=2022, start_month=3, 
                               end_year=2023, end_month=3)
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

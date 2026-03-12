#!/usr/bin/env python3
"""
Git Commit History Generator - Non-Interactive Version
This version runs without confirmation prompts.
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
        print(f"Error executing command: {e}")
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

def get_current_branch():
    """Get the current git branch name."""
    success, branch, _ = run_command("git rev-parse --abbrev-ref HEAD")
    if success:
        return branch.strip()
    return None

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
        
        success, _, stderr = run_command("git add activity_log.txt")
        if not success:
            return False
        
        iso_date = commit_date.isoformat()
        commit_message = f"Auto-generated commit #{commit_count}"
        
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = iso_date
        env["GIT_COMMITTER_DATE"] = iso_date
        
        cmd = f'git commit -m "{commit_message}"'
        success, _, stderr = run_command(cmd, env=env)
        
        return success
        
    except Exception as e:
        return False

def generate_commit_history(days=730):
    """Generate commit history for the past N days."""
    print("=" * 60)
    print("Git Commit History Generator (Non-Interactive Mode)")
    print("=" * 60)
    
    # Pre-flight checks
    print("\n[1/5] Running pre-flight checks...")
    
    if not check_git_initialized():
        print("✗ Not a git repository.")
        sys.exit(1)
    print("✓ Git repository detected")
    
    current_branch = get_current_branch()
    print(f"✓ Current branch: {current_branch}")
    
    if not check_uncommitted_changes():
        print("✗ Uncommitted changes detected. Commit or stash them first.")
        sys.exit(1)
    print("✓ No uncommitted changes")
    
    # Calculate total commits
    print("\n[2/5] Generating commit schedule...")
    total_commits = 0
    start_date = datetime.now()
    end_date = start_date - timedelta(days=days)
    
    current_date = end_date
    commits_per_day = {}
    
    while current_date <= start_date:
        num_commits = random.randint(2, 5)
        commits_per_day[current_date.date()] = num_commits
        total_commits += num_commits
        current_date += timedelta(days=1)
    
    print(f"✓ Scheduled {total_commits} commits across {days} days")
    print(f"  Average commits per day: {total_commits / days:.2f}")
    
    # Create commits
    print("\n[3/5] Creating commits (this may take a while)...")
    commit_count = 0
    failed_count = 0
    
    current_date = end_date
    while current_date <= start_date:
        num_commits = commits_per_day[current_date.date()]
        
        for i in range(num_commits):
            random_time = generate_random_commit_date(current_date)
            commit_datetime = datetime.fromisoformat(random_time)
            
            if create_commit(commit_datetime, commit_count + 1):
                commit_count += 1
                if commit_count % 50 == 0:
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
        # Change to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        if not check_git_initialized():
            print("Error: Not a git repository")
            sys.exit(1)
        
        print("Starting commit history generation...")
        generate_commit_history(days=730)
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

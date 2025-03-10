import os
import hashlib
import logging

# Newly created file: api_gateway_backup_and_recovery/backup_verification.py

def calculate_md5(file_path):
    """ Calculates the MD5 checksum of a file. """
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logging.error(f"Error calculating MD5 for {file_path}: {e}")
        return None

def verify_backup(files_to_verify, checksums):
    """
    Checks the accuracy and completeness of the backup data.
    Ensures all necessary files are backed up without any corruption.
    
    Parameters:
    files_to_verify (list): List of file paths to verify.
    checksums (dict): Dictionary with file paths as keys and their expected MD5 checksums as values.
    
    Returns:
    bool: True if all files are verified successfully, False otherwise.
    """
    if not files_to_verify or not checksums:
        logging.error("Verification failed due to missing file list or checksums.")
        return False

    all_verified = True
    
    for file_path in files_to_verify:
        expected_checksum = checksums.get(file_path)
        
        if expected_checksum is None:
            logging.error(f"No checksum found for file: {file_path}")
            all_verified = False
            continue
        
        actual_checksum = calculate_md5(file_path)
        
        if actual_checksum is None:
            logging.error(f"Could not calculate checksum for file: {file_path}")
            all_verified = False
            continue
        
        if actual_checksum != expected_checksum:
            logging.error(f"Checksum mismatch for file: {file_path}. Expected: {expected_checksum}, Actual: {actual_checksum}")
            all_verified = False
    
    if all_verified:
        logging.info("All files verified successfully.")
    else:
        logging.error("Backup verification failed.")
    
    return all_verified

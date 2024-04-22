import os
import subprocess
import shutil
import zipfile
import sys

def decompile_apk(apk_file, output_dir):
    # Use apktool to decompile the APK
    subprocess.run(['apktool', 'd', apk_file, '-o', output_dir, '-f'], check=True)

def modify_package_name(manifest_path, old_package_name, new_package_name):
    # Read the manifest file and replace the package name
    with open(manifest_path, 'r') as file:
        manifest_content = file.read()

    modified_manifest_content = manifest_content.replace(old_package_name, new_package_name)

    # Write the modified manifest back to the file
    with open(manifest_path, 'w') as file:
        file.write(modified_manifest_content)

def compile_apk(input_dir, output_file):
    # Use apktool to recompile the modified APK
    subprocess.run(['apktool', 'b', input_dir, '-o', output_file], check=True)

def rename_apk(output_apk, output_dir):
    # Get the base name of the output APK file
    apk_basename = os.path.basename(output_apk)

    # Append the desired string to the base name
    new_apk_basename = apk_basename.replace('.apk', '_renamed.apk')

    # Construct the path for the renamed APK file
    new_apk_file = os.path.join(output_dir, new_apk_basename)

    # Rename the output APK file
    os.rename(output_apk, new_apk_file)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python rename_apk_package.py <apk_file> <old_package_name> <new_package_name> <output_dir>")
        sys.exit(1)

    apk_file = sys.argv[1]
    old_package_name = sys.argv[2]
    new_package_name = sys.argv[3]
    output_dir = sys.argv[4]

    # Create a temporary directory for decompiled files
    temp_dir = os.path.join(output_dir, 'temp_decompile')
    decompile_apk(apk_file, temp_dir)

    # Modify the package name in the AndroidManifest.xml
    manifest_path = os.path.join(temp_dir, 'AndroidManifest.xml')
    modify_package_name(manifest_path, old_package_name, new_package_name)

    # Recompile the modified files into a new APK
    output_apk = os.path.join(output_dir, 'output.apk')
    compile_apk(temp_dir, output_apk)

    # Rename the output APK file
    rename_apk(output_apk, output_dir)

    # Clean up temporary directory
    shutil.rmtree(temp_dir)

    print("APK package name changed successfully!")

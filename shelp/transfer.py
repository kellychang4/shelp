from cloudpathlib import AnyPath, CloudPath


def transfer(source_destination, target_destination, force = False):
  ### create Paths from source and target destinations
  source_dest = AnyPath(source_destination)
  target_dest = AnyPath(target_destination)

  ### determine cloud directory and download/upload paths
  if isinstance(source_dest, CloudPath):
    print(f"Downloading '{source_dest}' to '{target_dest}'")
    source_dest.download_to(target_dest)
  else: # target is the CloudPath
    print(f"Uploading '{source_dest}' to '{target_dest}'")
    if force: # if forcing overwrite to cloud
      print("[INFO] Forcing overwrite to cloud upload!")
    target_dest.upload_from(source_dest, force_overwrite_to_cloud = force)
VHD="$(pwd)/storage_disk.img"
MOUNTP="$(pwd)/VHD"
LOOP=$(sudo losetup -j $VHD -O NAME | grep loop)

sudo umount $MOUNTP
echo "Unmounted disk: $MOUNTP"
sudo losetup -d $LOOP
echo "Detached loop: $LOOP"
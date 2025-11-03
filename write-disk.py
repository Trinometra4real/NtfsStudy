import os, sys
def reversebinary(buffer:bytes):
    temp = list(bytearray(buffer))
    temp.reverse()
    return bytes(bytearray(temp))


class DiskManagerNtfs:
    PARTITION_0 = [235, 82, 144, 78, 84, 70, 83, 32, 32, 32, 32, 0, 2, 8, 0, 0, 0, 0, 0, 0, 0, 248, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 0, 128, 0, 255, 15, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 246, 0, 0, 0, 1, 0, 0, 0, 166, 4, 115, 51, 205, 60, 231, 100, 0, 0, 0, 0, 14, 31, 190, 113, 124, 172, 34, 192, 116, 11, 86, 180, 14, 187, 7, 0, 205, 16, 94, 235, 240, 50, 228, 205, 22, 205, 25, 235, 254, 84, 104, 105, 115, 32, 105, 115, 32, 110, 111, 116, 32, 97, 32, 98, 111, 111, 116, 97, 98, 108, 101, 32, 100, 105, 115, 107, 46, 32, 80, 108, 101, 97, 115, 101, 32, 105, 110, 115, 101, 114, 116, 32, 97, 32, 98, 111, 111, 116, 97, 98, 108, 101, 32, 102, 108, 111, 112, 112, 121, 32, 97, 110, 100, 13, 10, 112, 114, 101, 115, 115, 32, 97, 110, 121, 32, 107, 101, 121, 32, 116, 111, 32, 116, 114, 121, 32, 97, 103, 97, 105, 110, 32, 46, 46, 46, 32, 13, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 85, 170]
    
    def __init__(self, disk_image_path: str):
        self.disk_image_path = disk_image_path
        with open(self.disk_image_path, "rb") as f:
            self.size = f.read(-1).__len__()
            f.seek(int.from_bytes(b'\x0B',"big"))
            self.bytes_per_sectors = int.from_bytes(reversebinary(f.read(2)), "big")
            f.seek(int.from_bytes(b'\x0D', "big"))
            self.sectors_per_clusters = int.from_bytes(f.read(1), "big")
            f.seek(int.from_bytes(b'\x0E', "big"))
            self.reserved_sectors = int.from_bytes(reversebinary(f.read(2)), "big")
            f.seek(int.from_bytes(b'\x1A', "big"))
            self.number_heads = int.from_bytes(reversebinary(f.read(2)), "big")
            f.seek(int.from_bytes(b'\x30', "big"))
            self.MFT_cluster_num = reversebinary(f.read(8))
            f.seek(int.from_bytes(b'\x38', "big"))
            self.MFT_Mirr_cluster_num = reversebinary(f.read(8))
            f.seek(int.from_bytes(b'\x40', "big"))
            self.clusters_per_file_record = int.from_bytes(reversebinary(f.read(4)), "big")
            f.seek(int.from_bytes(b'\x44', "big"))
            self.clusters_per_index_buffer=int.from_bytes(f.read(1), "big")
            
        self.max_sector = self.size // 512
        self.max_cluster = self.max_sector//self.sectors_per_clusters
        dizaine=0
        while (self.size>2**(dizaine*10)):
            dizaine+=1
        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        print("loaded disk of size: ", self.size/2**(10*(dizaine-1)), units[dizaine-1])

    def format(self):
        with open(self.disk_image_path, "wb") as f:
            f.seek(0)
            f.write(bytearray(self.PARTITION_0))
            f.seek((self.max_sector-1)*512)
            
    def read_sector(self, sector:int) -> bytes:
        with open(self.disk_image_path, "rb") as f:
            print("reading sector : ", sector,"->",sector+1, "/", self.max_sector)
            f.seek(512*sector)
            return f.read(512)
    
    def read_cluster(self, cluster:int):
        with open(self.disk_image_path, "rb") as f:
            print("reading cluster : ", cluster, "->", cluster+1, "/", self.max_cluster)
            f.seek(512*cluster*self.sectors_per_clusters)
            return f.read(512*self.sectors_per_clusters)
        
        
DMN = DiskManagerNtfs("./storage_disk.iso")
print("Bytes per sectors: ",DMN.bytes_per_sectors )
print("Sectors per clusters: ", DMN.sectors_per_clusters)
print("MTF file is located at sector: ", DMN.sectors_per_clusters*int.from_bytes(DMN.MFT_cluster_num, "big"))
print("MTF mirror is located at sector : ", DMN.sectors_per_clusters*int.from_bytes(DMN.MFT_Mirr_cluster_num, "big"))
data = DMN.read_sector(int(sys.argv[1]))
if data == b"":
    print("Sector out of buffer size")
    sys.exit(0)


buffer = []
final_table = []
for i in range(data.__len__()):
    if i % 16 == 0 and i != 0:
        final_table.append(buffer)
        buffer = []
        buffer.append(data[i])
    else:
        buffer.append(data[i])
final_table.append(buffer)

print("Offset(h) 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F")
print("---------------------------------------------------------")
for i in range(0, final_table.__len__()):
    line = ""
    decoded_line = b""
    for word in final_table[i]:
        decoded_line+=bytes(word)
        line += str(hex(word)).replace("0x", "").zfill(2).upper() +" "
    print(str(hex(int(sys.argv[1])*512+i*16)).zfill(8),"--",line+" "+decoded_line.decode("ASCII", errors="ignore"), sep="")
    
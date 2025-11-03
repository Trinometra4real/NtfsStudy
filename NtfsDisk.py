class NtfsDisk:  
    SECTOR_0 = [235, 82, 144, 78, 84, 70, 83, 32, 32, 32, 32, 0, 2, 8, 0, 0, 0, 0, 0, 0, 0, 248, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 0, 128, 0, 255, 15, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 246, 0, 0, 0, 1, 0, 0, 0, 166, 4, 115, 51, 205, 60, 231, 100, 0, 0, 0, 0, 14, 31, 190, 113, 124, 172, 34, 192, 116, 11, 86, 180, 14, 187, 7, 0, 205, 16, 94, 235, 240, 50, 228, 205, 22, 205, 25, 235, 254, 84, 104, 105, 115, 32, 105, 115, 32, 110, 111, 116, 32, 97, 32, 98, 111, 111, 116, 97, 98, 108, 101, 32, 100, 105, 115, 107, 46, 32, 80, 108, 101, 97, 115, 101, 32, 105, 110, 115, 101, 114, 116, 32, 97, 32, 98, 111, 111, 116, 97, 98, 108, 101, 32, 102, 108, 111, 112, 112, 121, 32, 97, 110, 100, 13, 10, 112, 114, 101, 115, 115, 32, 97, 110, 121, 32, 107, 101, 121, 32, 116, 111, 32, 116, 114, 121, 32, 97, 103, 97, 105, 110, 32, 46, 46, 46, 32, 13, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 85, 170]
    def reversebinary(buffer:bytes):
        temp = list(bytearray(buffer))
        temp.reverse()
        return bytes(bytearray(temp))
    
    def __init__(self, disk_image_path: str):
        self.disk_image_path = disk_image_path
        with open(self.disk_image_path, "rb") as f:
            self.size = f.read(-1).__len__()
            f.seek(int.from_bytes(b'\x0B'))
            self.bytes_per_sectors = int.from_bytes(NtfsDisk.reversebinary(f.read(2)))
            f.seek(int.from_bytes(b'\x0D'))
            self.sectors_per_clusters = int.from_bytes(f.read(1))
            f.seek(int.from_bytes(b'\x0E'))
            self.reserved_sectors = int.from_bytes(NtfsDisk.reversebinary(f.read(2)))
            f.seek(int.from_bytes(b'\x1A'))
            self.number_heads = int.from_bytes(NtfsDisk.reversebinary(f.read(2)))
            f.seek(int.from_bytes(b'\x30'))
            self.MFT_cluster_num = NtfsDisk.reversebinary(f.read(8))
            f.seek(int.from_bytes(b'\x38'))
            self.MFT_Mirr_cluster_num = NtfsDisk.reversebinary(f.read(8))
            f.seek(int.from_bytes(b'\x40'))
            self.clusters_per_file_record = int.from_bytes(NtfsDisk.reversebinary(f.read(4)))
            f.seek(int.from_bytes(b'\x44'))
            self.clusters_per_index_buffer=int.from_bytes(f.read(1))
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
            f.write(bytearray(self.SECTOR_0))
            f.seek((self.max_sector-1)*512)
            f.write(bytearray(self.SECTOR_0))

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
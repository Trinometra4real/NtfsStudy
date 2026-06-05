import os, sys, json
from io import BufferedReader, BytesIO
from filerec import *


class DiskManagerNtfs:
    
    EXCEPTION_IS_NOT_FILEREC=Exception("Sector pointed is not the start of a File Record")
    PARTITION_0 = [235, 82, 144, 78, 84, 70, 83, 32, 32, 32, 32, 0, 2, 8, 0, 0, 0, 0, 0, 0, 0, 248, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 0, 128, 0, 255, 15, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 246, 0, 0, 0, 1, 0, 0, 0, 166, 4, 115, 51, 205, 60, 231, 100, 0, 0, 0, 0, 14, 31, 190, 113, 124, 172, 34, 192, 116, 11, 86, 180, 14, 187, 7, 0, 205, 16, 94, 235, 240, 50, 228, 205, 22, 205, 25, 235, 254, 84, 104, 105, 115, 32, 105, 115, 32, 110, 111, 116, 32, 97, 32, 98, 111, 111, 116, 97, 98, 108, 101, 32, 100, 105, 115, 107, 46, 32, 80, 108, 101, 97, 115, 101, 32, 105, 110, 115, 101, 114, 116, 32, 97, 32, 98, 111, 111, 116, 97, 98, 108, 101, 32, 102, 108, 111, 112, 112, 121, 32, 97, 110, 100, 13, 10, 112, 114, 101, 115, 115, 32, 97, 110, 121, 32, 107, 101, 121, 32, 116, 111, 32, 116, 114, 121, 32, 97, 103, 97, 105, 110, 32, 46, 46, 46, 32, 13, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 85, 170]
    MAPPED_PRIMARY_FR ={}
    root_file={".":[

    ]}
    
    def __init__(self, disk_image_path: str):
        self.root={}
        self.disk_image_path = disk_image_path
        with open(self.disk_image_path, "rb") as f:

            self.size = f.read(-1).__len__()

            f.seek(int.from_bytes(b'\x0B',"big"))
            self.bytes_per_sectors = int.from_bytes(reversebinary(f.read(2)), "big")

            
            self.sector_per_filerec=1024//self.bytes_per_sectors

            f.seek(int.from_bytes(b'\x0D', "big"))
            self.sectors_per_clusters = int.from_bytes(f.read(1), "big")

            
            f.seek(int.from_bytes(b'\x0E', "big"))
            self.reserved_sectors = int.from_bytes(reversebinary(f.read(2)), "big")

            f.seek(int.from_bytes(b'\x1A', "big"))
            self.number_heads = int.from_bytes(reversebinary(f.read(2)), "big")

            f.seek(int.from_bytes(b'\x30', "big"))
            self.MFT_cluster_num = int.from_bytes(reversebinary(f.read(8)), "big")

            f.seek(int.from_bytes(b'\x38', "big"))
            self.MFT_Mirr_cluster_num = int.from_bytes(reversebinary(f.read(8)), "big")

            f.seek(int.from_bytes(b'\x40', "big"))
            self.clusters_per_file_record = int.from_bytes(reversebinary(f.read(4)), "big")

            f.seek(int.from_bytes(b'\x44', "big"))
            self.clusters_per_index_buffer=int.from_bytes(f.read(1), "big")
            
        self.max_sector = self.size // self.bytes_per_sectors
        self.max_cluster = self.max_sector//self.sectors_per_clusters
        dizaine=0
        while (self.size>2**(dizaine*10)):
            dizaine+=1
        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        print("loaded disk of size: ", self.size/2**(10*(dizaine-1)), units[dizaine-1])

    def loadBitmaprec(self):
        datarun=self.MAPPED_PRIMARY_FR["$Bitmap"]["$DATA"]["attr_var"]["data_run"][0]

        offset =int.from_bytes(bytes.fromhex(datarun["cluster_offset"].replace("0x", "")))
        length =int.from_bytes(bytes.fromhex(datarun["length"].replace("0x", "")))
        with open(self.disk_image_path, "rb") as f:
            f.seek(offset*self.sectors_per_clusters*self.bytes_per_sectors)
            self.bitmap=f.read(length*self.sectors_per_clusters*self.bytes_per_sectors)

    def loadRootFolder(self):
        self.walkFilePath("/")
    def loadIndex(self):
        pass
    
    def parseIndxRecord(self, offset_to_indx:int, length:int):
        indx={}
        INDX=None
        CLUSTER=None
        isINDX=False
        viable_clusters=[]
        with open(self.disk_image_path, "rb") as f:
            f.seek(offset_to_indx)
            CLUSTER=f.read(self.bytes_per_sectors*self.sectors_per_clusters*length)
            f.seek(offset_to_indx)
            isINDX=(f.read(4).hex()=="494e4458")
            f.close()
        
        offset=0
        if isINDX:
            f=BytesIO(CLUSTER)
            usa_array=[]
            offset=4     
              
            f.seek(offset)
            USA_offset=reversebinary(f.read(2))
            offset+=2

            f.seek(offset)
            USA_count=int.from_bytes(reversebinary(f.read(2)))
            offset+=2

            f.seek(offset)
            logfile_seq_num=f.read(8)
            offset+=8

            f.seek(offset)
            vcn=f.read(8)
            offset+=8
            # Index_Header
            index_header_offset=offset
            header={}
            header.update({
                "usa_offset":USA_offset.hex(),
                "usa_count":USA_count,
                "logfile":logfile_seq_num.hex(),
                "vcn":vcn.hex()
            })

            f.seek(offset)
            entries_offset=reversebinary(f.read(4))
            first_entry=int.from_bytes(entries_offset)+offset
            offset+=4

            f.seek(offset)
            index_length=int.from_bytes(reversebinary(f.read(4))) # in bytes
            offset+=4

            f.seek(offset)
            allocated_size=reversebinary(f.read(4))
            offset+=4

            f.seek(offset)
            flag=f.read(1)
            offset+=1
            
            offset=int.from_bytes(USA_offset)
            
            f.seek(offset)
            usn = f.read(2)
            offset+=2
            
            f.seek(offset)
            
            for i in range(1, USA_count+1):
                f.seek(offset)
                arraybuffer=bytearray(CLUSTER)
                if arraybuffer[i*self.bytes_per_sectors-2:i*self.bytes_per_sectors]!=bytearray(b''):
                    viable_clusters.append(arraybuffer[i*self.bytes_per_sectors-2:i*self.bytes_per_sectors]==bytearray(usn))
                else:
                    viable_clusters.append(False)
                
                if arraybuffer[i*self.bytes_per_sectors-2:i*self.bytes_per_sectors]==usn:
                    arraybuffer[i*self.bytes_per_sectors-2:i*self.bytes_per_sectors]=f.read(2)
                    
                CLUSTER=bytes(arraybuffer)
                offset+=2
            
            f=BytesIO(CLUSTER)

            offset=first_entry
            saved_offset=offset
            notEmpty=True
            
            while notEmpty:
                
                # INDEX_ENTRY
                file={}
                f.seek(offset)
                fileref = reversebinary(f.read(8)) # offset 0x00
                file["fileref"]=fileref.hex()
                offset+=8
                g=BytesIO(fileref)
                g.seek(0)
                seq_num=g.read(2)
                g.seek(2)
                mft_record=g.read(6)
                g.close()

                file["seq_num"]=seq_num.hex()
                file["mft_record"]=mft_record.hex()
                f.seek(offset)
                entry_length=int.from_bytes(reversebinary(f.read(2))) # offset 0x08
                offset+=2

                f.seek(offset)
                key_length=int.from_bytes(reversebinary(f.read(2))) # offset 0x0A
                offset+=2

                f.seek(offset)
                entry_flags=reversebinary(f.read(2)) # offset 0x0C
                offset+=2
                
                if int.from_bytes(entry_flags) & 0x02:
                    notEmpty=False
                    break

                offset+=2 # Padding

                # FILE NAME KEY

                f.seek(offset)
                parent_dir_ref=reversebinary(f.read(8))
                offset+=8

                
                file["parent_dir_ref"]=parent_dir_ref.hex()

                f.seek(offset)
                creation_time=reversebinary(f.read(8))
                offset+=8

                file["creation_time"]=int.from_bytes(creation_time)

                f.seek(offset)
                file_edit_time=reversebinary(f.read(8))
                file["file_edit_time"]=int.from_bytes(file_edit_time)
                offset+=8

                f.seek(offset)
                mft_edit_time=reversebinary(f.read(8))
                offset+=8

                file["mft_edit_time"]=int.from_bytes(mft_edit_time)

                f.seek(offset)
                accessed_time=reversebinary(f.read(8))
                offset+=8

                file["accessed_time"]=int.from_bytes(accessed_time)

                f.seek(offset)
                allocated_size=reversebinary(f.read(8))
                offset+=8

                file["allocated_size"]=allocated_size.hex()

                f.seek(offset)
                real_size=reversebinary(f.read(8))
                offset+=8

                file["real_size"]=real_size.hex()

                f.seek(offset)
                file_attr=reversebinary(f.read(4))
                offset+=4

                file["file_attr"]=file_attr.hex()

                f.seek(offset)
                ea_reparse_val=f.read(4)
                offset+=4

                file["ea_reparse_val"]=ea_reparse_val.hex()

                f.seek(offset)
                filename_length=f.read(1)
                offset+=1

                file["filename_length"]=int.from_bytes(filename_length)

                f.seek(offset)
                filename_namespace=f.read(1)
                offset+=1

                file["filename_namespace"]=filename_namespace.hex()

                f.seek(offset)
                filename=f.read(2*int.from_bytes(filename_length)).decode("UTF-16LE")
                offset+=2*int.from_bytes(filename_length)

                file["name"]=filename
                
                file["end_offset"]=saved_offset+entry_length
                indx[file["name"]]=file
                saved_offset+=entry_length
                offset=saved_offset
            return indx
        else:
            return None


    def walkFilePath(self, path)-> list|None:
        indx={}
        header={}
        
        if (path=="/"):
            data_run=self.MAPPED_PRIMARY_FR["."]["$INDEX_ALLOCATION"]["attr_var"]["data_run"][0]
            offset_to_indx=int.from_bytes(bytes.fromhex(data_run["cluster_offset"].replace("0x", "")))*self.sectors_per_clusters*self.bytes_per_sectors

            self.root=self.parseIndxRecord(offset_to_indx, int.from_bytes(bytes.fromhex(data_run["length"].replace("0x", ""))))
            return self.root
        else:
            absolute_path = path.split("/")
            absolute_path[0]="."
            print(absolute_path)
            index_found=self.root.copy()
            for i in range(0, absolute_path.__len__()-1):
                if absolute_path[i] in index_found.keys():
                    file_info=index_found[absolute_path[i]]
                    mftrec_num=int.from_bytes(bytes.fromhex(file_info["mft_record"]))
                    print("Searching at mftrec num=", mftrec_num)
                    filerec_mapp = self.locateFileContent(mftrec_num)
                    with open("dumpIndex.json", 'w') as h:
                        h.write(json.dumps(filerec_mapp))
                    
                    
                    if "$INDEX_ALLOCATION" in filerec_mapp.keys():
                        data_run=filerec_mapp["$INDEX_ALLOCATION"]["attr_var"]["data_run"][0]
                        offset_to_indx=int.from_bytes(bytes.fromhex(data_run["cluster_offset"].replace("0x", "")))*self.sectors_per_clusters*self.bytes_per_sectors
                        print("Allocation index found")
                        index_found=self.parseIndxRecord(offset_to_indx, int.from_bytes(bytes.fromhex(data_run["length"].replace("0x", ""))))
                        

                    elif "$INDEX_ROOT" in filerec_mapp.keys():
                        print("Root index found")
                        index_found=filerec_mapp["$INDEX_ROOT"]["attr_var"]["index_entries"]
                    else:
                        print("No index found")
                    
                else:
                    print("file '", absolute_path[i], "' not found at location "+path)
                    return None
        return index_found[absolute_path[-1]]
    
    def locateFileContent(self, mft_record:int):
        print("self cluster num is ",self.MFT_cluster_num)
        offset_sector=self.sector_per_filerec*mft_record+self.MFT_cluster_num*self.sectors_per_clusters
        offset_bytes=offset_sector*self.bytes_per_sectors
        print("searching at offset : ", offset_bytes, "(sector num°", offset_sector, ")")
        f=open(self.disk_image_path, "rb")
        asked_file=FileRecord(f, offset_bytes, self.bytes_per_sectors*self.sector_per_filerec)
        f.close()
        if (asked_file.is_filerec):
            return asked_file.Attributes
        else:
            print("Researched item is not a filerec")


    def format(self):
        with open(self.disk_image_path, "wb") as f:
            f.seek(0)
            f.write(bytearray(self.PARTITION_0))
            f.seek((self.max_sector-1)*self.bytes_per_sectors)
            
    def read_sector(self, sector:int) -> bytes:
        with open(self.disk_image_path, "rb") as f:
            print("reading sector : ", sector,"->",sector+1, "/", self.max_sector)
            f.seek(self.bytes_per_sectors*sector)
            return f.read(self.bytes_per_sectors)
    
    def read_cluster(self, cluster:int):
        with open(self.disk_image_path, "rb") as f:
            print("reading cluster : ", cluster, "->", cluster+1, "/", self.max_cluster)
            f.seek(self.bytes_per_sectors*cluster*self.sectors_per_clusters)
            return f.read(self.bytes_per_sectors*self.sectors_per_clusters)
    
    def read_fileRec(self, sector:int):
        startingpoint=self.bytes_per_sectors*sector
        with open(self.disk_image_path, "rb") as f:
            f.seek(startingpoint)
            print(f.read(4), " is it magic number ?")
        
    def dumpAttributes(self, sector:int, path:str)->FileRecord:
        filerec = FileRecord(
            open(self.disk_image_path, "rb"), 
            sector*self.bytes_per_sectors,
            self.bytes_per_sectors*self.sector_per_filerec
            )
        if (filerec.is_filerec):
            print("Filerec size is: ", filerec.filerec_real_size_str)
            print("Filerec allocated size is: ", filerec.allocated_size_of_filerec_str)
            with open(path, "w") as f:
                f.write(
                    json.dumps(filerec.getAttributes())
                    )
            return filerec
        else:
            raise DiskManagerNtfs.EXCEPTION_IS_NOT_FILEREC
    
    def loadPrimaryFr(self):
        FRoffset=self.MFT_cluster_num*self.sectors_per_clusters*self.bytes_per_sectors
        for i in range(0, 12):

            filerecord = FileRecord(open(self.disk_image_path, "rb"), FRoffset, self.bytes_per_sectors*self.sector_per_filerec)
            FRoffset+=2*self.bytes_per_sectors
            self.MAPPED_PRIMARY_FR.update({filerecord.Attributes["$FILE_NAME"]["attr_var"]["filename"]:filerecord.Attributes})
        print("Mapped ",self.MAPPED_PRIMARY_FR.keys().__len__(), " filerec")
        with open("dumpDiskManagerFileRecs.json", "w") as f:
            f.write(json.dumps(self.MAPPED_PRIMARY_FR))
        data_run=self.MAPPED_PRIMARY_FR["."]["$INDEX_ALLOCATION"]["attr_var"]["data_run"][0]
        offset_to_indx=int.from_bytes(bytes.fromhex(data_run["cluster_offset"].replace("0x", "")))*self.sectors_per_clusters*self.bytes_per_sectors

        self.root=self.parseIndxRecord(offset_to_indx, int.from_bytes(bytes.fromhex(data_run["length"].replace("0x", ""))))

    def scrawl_disk(self, wordlist_magic_number:dict):
        with open(self.disk_image_path, "rb") as f:
            pass
        hex_sign=0


DMN = DiskManagerNtfs("./storage_disk.img")
print("Bytes per sectors: ",DMN.bytes_per_sectors )
print("Sectors per clusters: ", DMN.sectors_per_clusters)
print("MTF file is located at sector: ", DMN.sectors_per_clusters*DMN.MFT_cluster_num)
print("MTF mirror is located at sector : ", DMN.sectors_per_clusters*DMN.MFT_Mirr_cluster_num)

data = DMN.read_sector(int(sys.argv[1]))

if data == b"":
    print("Sector out of buffer size")
    sys.exit(0)
DMN.loadPrimaryFr()
DMN.loadBitmaprec()
with open("dumprootfiles.json", "w") as f:
    f.write(json.dumps(DMN.walkFilePath("/")))

def test():
    try : 
        filerec = DMN.dumpAttributes(int(sys.argv[1]), "dumpsAttributes.json")
        print("Reading file record")
    except Exception as e:
        print(e)

test()

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
try:
    print(DMN.walkFilePath("/test_folder/insider/treated_2026-04-03.zip"))
except:
    pass

print("Offset(h) 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F")
print("---------------------------------------------------------")

for i in range(0, final_table.__len__()):
    line = ""
    decoded_line = ""
    for word in final_table[i]:
        
        line += str(hex(word)).replace("0x", "").zfill(2).upper() +" "
        if (word>=32 and word<=125):
            decoded_line+=(int.to_bytes(word).decode("ASCII"))
        else:
            decoded_line+="."

    print(str(hex(int(sys.argv[1])*DMN.bytes_per_sectors+i*16)).zfill(8),"--",line+" "+decoded_line, sep="")


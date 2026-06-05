from io import BufferedReader, BytesIO
from datetime import datetime, timedelta


def reversebinary(buffer:bytes):
    temp = list(bytearray(buffer))
    temp.reverse()
    return bytes(bytearray(temp))
class Attribute:
    type_str=""
    type_=0
    length_=0
    attr_map={}
    mapp={}

    @staticmethod
    def parseI30(bytes_buffer)->dict:
        f=BytesIO(bytes_buffer)
        index={}
        offset=0
        saved_offset=0
        
        
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
        file["entry_flag"]=entry_flags.hex()
        

        if (entry_length==24):
            
            file["type"]="VCN"
            f.seek(offset)
            VCN=reversebinary(f.read(8))
            file["VCN"]="0x"+VCN.hex()
            file["end_offset"]=saved_offset+entry_length
            index["vcn"]=file
            
            
        else:
            offset+=2 # Padding
            file["type"]="FILE_NAME"
            
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
            index[filename]=file
            file["end_offset"]=saved_offset+entry_length
            

        
        return index

    def __init__(self, f:BufferedReader, init_attr_offset:int):
        self.attr_mapp={}
        self.mapp={}
        content={}
        offset=init_attr_offset
        
        
        content.update({"offset":"0x"+offset.to_bytes(4, 'big', signed=False).hex()})
        f.seek(offset)
        raw_type=reversebinary(f.read(4)) # offset 00
        type_=int.from_bytes(raw_type)
        offset+=4
        
        if (type_==16):
            type_str="$STANDARD_INFORMATION"
        elif (type_==2*16):
            type_str="$ATTRIBUTE_LIST"
        elif type_==(3*16):
            type_str="$FILE_NAME"
        elif type_==(4*16):
            type_="$OBJECT_ID"
        elif type_==(5*16):
            type_str="$SECURITY_DESCRIPTOR"
        elif type_==(6*16):
            type_str="$VOLUME_NAME"
        elif type_==(7*16):
            type_str="$VOLUME_INFORMATION"
        elif type_==(8*16):
            type_str="$DATA"
        elif type_==(9*16):
            type_str="$INDEX_ROOT"
        elif type_==(10*16):
            type_str="$INDEX_ALLOCATION"
        elif type_==(11*16):
            type_str="$BITMAP"
        elif type_==(12*16):
            type_str="$REPARSE_POINT"
        elif type_==(13*16):
            type_str="$EA_INFORMATION"
        elif type_==(14*16):
            type_str="$EA"
        elif type_==(15*16):
            type_str="$PROPERTY_SET"
        elif type_==(16**2):
            type_str="$LOGGED_UTILITY_STREAM"
        else:
            type_str="$"+type_.to_bytes(2, 'big', signed=False).hex()
        content.update({"type":type_str})
        f.seek(offset)
        length_=int.from_bytes(reversebinary(f.read(4))) # offset 04
        content.update({"length": length_})
        max_offset=init_attr_offset+length_
        content.update({"max_offset": "0x"+max_offset.to_bytes(4, 'big', signed=False).hex()})
        offset+=4

        f.seek(offset)
        non_resident_flag=f.read(1) # offet 08
        offset+=1
        content.update({"resident": int.from_bytes(non_resident_flag)==0})
        
        f.seek(offset)
        name_length=int.from_bytes(f.read(1)) # offset 09
        offset+=1
        content.update({"name_length": name_length})
        f.seek(offset)
        name_offset=int.from_bytes(reversebinary(f.read(2)))# offset 0A
        offset+=2
        content.update({"name_offset": name_offset}) 

        f.seek(offset)
        Flags=reversebinary(f.read(2)) # offset 0C
        offset+=2
        content.update({"Flags": "0x"+Flags.hex()})

        f.seek(offset)
        attr_id=reversebinary(reversebinary(f.read(2)))# offset 0E
        offset+=2 # offset 10
        content.update({"attr_id": "0x"+attr_id.hex()})

        if (int.from_bytes(non_resident_flag)==0):
            f.seek(offset)
            attr_lenght=int.from_bytes(reversebinary(f.read(4))) # offset 10
            offset+=4
            content.update({"attr_length":attr_lenght})

            f.seek(offset)
            attr_offset=int.from_bytes(reversebinary(f.read(2))) # offset 14
            offset+=2
            content.update({"attr_offset":attr_offset})


            f.seek(offset)
            indexed_flag=f.read(1) # offset 16
            content.update({"indexed_flag": "0x"+indexed_flag.hex()})
            offset+=1
            
            if (name_offset==0):
                name=None
            else:
                offset=name_offset+init_attr_offset
                f.seek(offset)
                name=f.read(name_length*2)
                content.update({"attr_name": name.decode("utf-16LE")})

            offset=init_attr_offset+attr_offset
        else:
            f.seek(offset)
            starting_vcn=reversebinary(f.read(8)) # offset 10
            offset+=8
            content.update({"starting_vcn":"0x"+starting_vcn.hex()})

            f.seek(offset)
            last_vcn=reversebinary(f.read(8)) # offset 18
            offset+=8
            content.update({"last_vcn":"0x"+last_vcn.hex()})

            f.seek(offset)
            offset_datarun=reversebinary(f.read(2)) # offset 20
            offset+=2
            content.update({"offset_datarun": "0x"+offset_datarun.hex()})

            f.seek(offset)
            compression_unit_size=reversebinary(f.read(2)) # offset 22
            offset+=6 # (4 bytes of padding)
            content.update({"compression_unit_size": int.from_bytes(compression_unit_size)})

            f.seek(offset)
            attribute_real_size=int.from_bytes(reversebinary(f.read(8))) # offset 28
            dizaine=0
            offset +=8
            while (attribute_real_size>2**(dizaine*10)):
                dizaine+=1 
            if (attribute_real_size==0):
                dizaine=1
            units = ["B", "KB", "MB", "GB", "TB", "PB"]
            content.update({"attr_real_size":str(attribute_real_size/2**(10*(dizaine-1)))+units[dizaine-1]})

            f.seek(offset)
            init_stream_data_size=int.from_bytes(reversebinary(f.read(8)))
            offset=init_attr_offset+int.from_bytes(offset_datarun)
            dizaine=0
            while (init_stream_data_size>2**(dizaine*10)):
                dizaine+=1 
            if (init_stream_data_size==0):
                dizaine=1
            units = ["B", "KB", "MB", "GB", "TB", "PB"]
            content.update({"init_stream_data_size":str(init_stream_data_size/2**(10*(dizaine-1)))+units[dizaine-1]})
            
        self.mapp.update({"attr_header":content})

        attr_values={}
        if (type_==16): # STANDARD_INFORMATION
            pass
        elif type_==(2*16): # ATTRIBUTE_LIST
            pass
        elif type_==(3*16): # FILE_NAME
            f.seek(offset)
            file_ref_2_parent_dir = f.read(8)
            attr_values.update({"file_ref_2_parent_dir":"0x"+file_ref_2_parent_dir.hex()})
            offset+=8

            f.seek(offset)
            ctime=reversebinary(f.read(8))
            ctime_date=datetime(1601, 1, 1) + timedelta(microseconds=int.from_bytes(ctime)/10)
            attr_values.update({"ctime":ctime_date.isoformat()})
            offset+=8

            f.seek(offset)
            atime=reversebinary(f.read(8))
            atime_date=datetime(1601, 1, 1) + timedelta(microseconds=int.from_bytes(atime)/10)
            attr_values.update({"atime":atime_date.isoformat()})
            offset+=8

            f.seek(offset)
            mtime=reversebinary(f.read(8))
            mtime_date=datetime(1601, 1, 1) + timedelta(microseconds=int.from_bytes(mtime)/10)
            attr_values.update({"mtime":mtime_date.isoformat()})
            offset+=8

            f.seek(offset)
            rtime=reversebinary(f.read(8))
            rtime_date=datetime(1601, 1, 1) + timedelta(microseconds=int.from_bytes(rtime)/10)
            attr_values.update({"rtime":rtime_date.isoformat()})
            offset+=8

            f.seek(offset)
            file_allocated_size=int.from_bytes(reversebinary(f.read(8)))
            dizaine=0
            while (file_allocated_size>2**(dizaine*10)):
                dizaine+=1 
            if (file_allocated_size==0):
                dizaine=1
            units = ["B", "KB", "MB", "GB", "TB", "PB"]
            attr_values.update({"file_allocated_size":str(file_allocated_size/2**(10*(dizaine-1)))+units[dizaine-1]})
            offset+=8

            f.seek(offset)
            file_real_size=int.from_bytes(reversebinary(f.read(8)))
            dizaine=0
            while (file_real_size>2**(dizaine*10)):
                dizaine+=1 
            units = ["B", "KB", "MB", "GB", "TB", "PB"]
            if (file_real_size==0):
                dizaine=1
            attr_values.update({"file_real_size":str(file_real_size/2**(10*(dizaine-1)))+units[dizaine-1]})
            offset+=8

            f.seek(offset)
            Flags=f.read(4)
            attr_values.update({"Flags": "0x"+Flags.hex()})
            offset+=4

            f.seek(offset)
            ea_reparse_data=f.read(4)
            attr_values.update({"Flags": "0x"+ea_reparse_data.hex()})
            offset+=4

            f.seek(offset)
            filename_length=int.from_bytes(f.read(1))
            attr_values.update({"filename_length":filename_length})
            offset+=1

            f.seek(offset)
            file_namespace=f.read(1)
            attr_values.update({"file_namespace":"0x"+file_namespace.hex()})
            offset+=1

            f.seek(offset)
            file_name=f.read(filename_length*2).decode("UTF-16LE")
            attr_values.update({"filename":file_name})
            offset+=filename_length*2



        elif type_==(5*16): # SECURITY_DESCRIPTOR
            pass

        elif type_==(6*16): # VOLUME_NAME
            pass

        elif type_==(7*16): # VOLUME_INFORMATION
            pass
            
        elif type_==(8*16): # DATA
            type_str="$DATA"
            data=None
            f.seek(offset)
            if int.from_bytes(non_resident_flag)==0:
                data=f.read(attr_lenght)
                try: data = data.decode()
                except:data="0x"+data.hex()
                attr_values.update({"data":data})
            else:
                data_run=[]
                i=0
                header=b'\xff'
                f.seek(offset)
                header=f.read(1)
                while header!=b'\x00':
                    
                    offset+=1
                    lowerbits=int.from_bytes(header)%16
                    upperbits=(int.from_bytes(header)-lowerbits)//16

                    f.seek(offset)
                    length=reversebinary(f.read(lowerbits))
                    offset+=lowerbits

                    f.seek(offset)
                    cluster_offset=reversebinary(f.read(upperbits))
                    offset+=upperbits
                    data_run.append({
                        "header": "0x"+header.hex(),
                        "length":"0x"+length.hex(),
                        "cluster_offset":"0x"+cluster_offset.hex()

                    })
                    f.seek(offset)
                    header=f.read(1)

                attr_values.update({"data_run":data_run})
                    
                    


                
                
                
        elif type_==(9*16): # INDEX_ROOT offset 0x5548
            index_root={}
            index_root_offset=offset
            f.seek(offset)
            
            entry_attribute_type=reversebinary(f.read(4))
            index_root.update({"attr_type":"0x"+entry_attribute_type.hex()})
            offset+=4

            f.seek(offset)
            collation_rule=reversebinary(f.read(4))
            index_root.update({"collation_rule":"0x"+collation_rule.hex()})
            offset+=4

            f.seek(offset)
            index_size_allocation=int.from_bytes(reversebinary(f.read(4)))
            index_root.update({"index_size_allocation":index_size_allocation})
            offset+=4

            f.seek(offset)
            cluster_per_index_record=int.from_bytes(reversebinary(f.read(4)))
            index_root.update({"cluster_per_index_record":cluster_per_index_record})
            offset+=4 # 3 bytes of padding

            saved_offset_header=offset
            index_header={}
            f.seek(offset)
            offset_to_first_entry=reversebinary(f.read(4))
            index_header.update({"offset_to_first_entry":"0x"+offset_to_first_entry.hex()})
            offset+=4

            f.seek(offset)
            total_indexentries_size=int.from_bytes(reversebinary(f.read(4)))
            index_header.update({"total_indexentries_size":total_indexentries_size})
            offset+=4

            f.seek(offset)
            allocated_size=int.from_bytes(reversebinary(f.read(4)))
            index_header.update({"allocated_size":allocated_size})
            offset+=4

            f.seek(offset)
            Flags=reversebinary(f.read(1))
            index_header.update({"Flags":"0x"+Flags.hex()})
            offset+=4 # 3 bytes of padding
            
            index_entries={}
            offset=saved_offset_header+int.from_bytes(offset_to_first_entry)
            saved_offset=offset
            # First Entry 0x5568
            
            if (content["attr_name"]=="$I30"):
                while True:
                    f.seek(offset+8)
                    entry__len__ = int.from_bytes(reversebinary(f.read(2)))
                    f.seek(offset)
                    attr_entry=Attribute.parseI30(f.read(entry__len__))
                    
                    
                    f.seek(offset+12)
                    flag=f.read(1)
                    offset+=entry__len__
                  
                    if (int.from_bytes(flag) & 0x02):
                        break
                    if (int.from_bytes(flag)==0 or int.from_bytes(flag) & 0x01):
                        index_entries.update(attr_entry)
            else:
                for i in range(0, total_indexentries_size//allocated_size):
                   while True:
                    f.seek(offset+8)
                    entry__len__ = int.from_bytes(reversebinary(f.read(2)))
                    f.seek(offset)
                    index_entries.update({"content" :f.read(entry__len__).hex()})
                    
                    
                    f.seek(offset+12)
                    flag=f.read(1)
                    offset+=entry__len__
                    if (int.from_bytes(flag) & 0x02):
                        break


            attr_values.update({"index_root":index_root})
            attr_values.update({"index_header":index_header})
            attr_values.update({"index_entries":index_entries})


            pass
        elif type_==(10*16): # INDEX_ALLOCATION
            data_run=[]
            i=0
            header=b'\xff'
            f.seek(offset)
            header=f.read(1)
            while header!=b'\x00':
                
                offset+=1
                lowerbits=int.from_bytes(header)%16
                upperbits=(int.from_bytes(header)-lowerbits)//16

                f.seek(offset)
                length=reversebinary(f.read(lowerbits))
                offset+=lowerbits

                f.seek(offset)
                cluster_offset=reversebinary(f.read(upperbits))
                offset+=upperbits
                data_run.append({
                    "header": "0x"+header.hex(),
                    "length":"0x"+length.hex(),
                    "cluster_offset":"0x"+cluster_offset.hex()

                })
                f.seek(offset)
                header=f.read(1)

            attr_values.update({"data_run":data_run})

        elif type_==(11*16): # BITMAP
            pass

        elif type_==(12*16): # REPARSE_POINT
            pass

        elif type_==(13*16): # EA_INFORMATION
            pass
        
        elif type_==(14*16): # EA
            pass

        elif type_==(15*16): 
            pass

        elif type_==(16*16): # LOGGED_UTILITY_STREAM
            pass

        self.mapp.update({"attr_var":attr_values})
        self.attr_mapp={type_str:self.mapp}
        

class FileRecord:
    Attributes={}
    offset_to_update_sequence=0
    size_in_words_of_update_sequence_array=0
    logfile_sequence_number=0
    sequence_number=0
    hardlink_count=0
    offset_2_first_attribute=0
    filerec_real_size=0
    allocated_size_of_filerec=0
    fileref_to_base_filerec=0
    next_attr_id=0
    is_filerec=False
    is_file=False
    is_directory=False
    def __init__(self, f:BufferedReader, offset:int, size:int):
        self.Attributes={}
        startingpoint=0+offset

        f.seek(offset)
        file_rec=f.read(size)

        f = BytesIO(file_rec)
        f.seek(int.from_bytes(b'\x30'))
        usn = f.read(2)
        f.seek(int.from_bytes(b'\x32'))
        replace_one=f.read(2)
        f.seek(int.from_bytes(b'\x34'))
        replace_two=f.read(2)

        buffer_array = bytearray(file_rec)
        self.is_filerec=(bytes(buffer_array[512-2:512])==bytearray(usn))
        print("buffer is :",buffer_array[512-2:512])
        print("usn is: ", usn)
        if (buffer_array[512-2:512]==bytearray(usn)):
            buffer_array[512-2:512] = bytearray(replace_one)
        
        print("buffer is :",buffer_array[512-2:512])
        if (buffer_array[1024-2:1024]==bytearray(usn)):
            buffer_array[1024-2:1024]=bytearray(replace_two)

        print("is it filerec ? : ", self.is_filerec)
        file_rec = bytes(buffer_array)
        f = BytesIO(file_rec)
        startingpoint=0
        offset=0
        f.seek(startingpoint)
        raw=f.read(4)
        try:
            self.is_filerec=(raw.decode("ASCII") == "FILE")
        except:
            self.is_filerec=False
        if (self.is_filerec):
            startingpoint+=4# 0-4 -> is FILE Magic Number

            f.seek(startingpoint) # offset 0x04
            self.offset_to_update_sequence=int.from_bytes(reversebinary(f.read(2)))
            startingpoint+=2

            f.seek(startingpoint) # offset 0x06
            self.size_in_words_of_update_sequence_array=int.from_bytes(reversebinary(f.read(2))) #  	Size in words of Update Sequence Number & Array (S)
            startingpoint+=2

            f.seek(startingpoint) # offset 0x08
            self.logfile_sequence_number=reversebinary(f.read(8))
            startingpoint+=8

            f.seek(startingpoint) # offset 0x10
            self.sequence_number=int.from_bytes(reversebinary(f.read(2)))
            startingpoint+=2

            f.seek(startingpoint) # offset 0x12
            self.hardlink_count=int.from_bytes(reversebinary(f.read(2)))
            startingpoint+=2

            f.seek(startingpoint) # offset 0x14
            self.offset_2_first_attribute=reversebinary(f.read(2))
            startingpoint+=2

            f.seek(startingpoint) # offset 0x16
            self.flags=int.from_bytes(reversebinary(f.read(2)))
            startingpoint+=2

            if ((self.flags%2)==1):
                self.is_inuse=True
                
            if ((self.flags-(self.flags%2))%4==2):
                self.is_directory=True
            else:
                self.is_file=True

            f.seek(startingpoint) # offset 0x18
            self.filerec_real_size=int.from_bytes(reversebinary(f.read(4)))
            dizaine=0
            while (self.filerec_real_size>2**(dizaine*10)):
                dizaine+=1 
            units = ["B", "KB", "MB", "GB", "TB", "PB"]
            self.filerec_real_size_str=str(self.filerec_real_size/2**(10*(dizaine-1)))+units[dizaine-1]
            startingpoint+=4

            f.seek(startingpoint) # offset 0x1C
            self.allocated_size_of_filerec=int.from_bytes(reversebinary(f.read(4)))
            while (self.allocated_size_of_filerec>2**(dizaine*10)):
                dizaine+=1 
            units = ["B", "KB", "MB", "GB", "TB", "PB"]
            self.allocated_size_of_filerec_str=str(self.allocated_size_of_filerec/2**(10*(dizaine-1)))+units[dizaine-1]
            startingpoint+=4

            f.seek(startingpoint) # offset 0x20
            self.fileref_to_base_filerec=reversebinary(f.read(8))
            startingpoint+=8

            f.seek(startingpoint) # offset 0x28
            self.next_attr_id=reversebinary(f.read(2))
            startingpoint+=2

            startingpoint+=2 # offset 0x2A -> Alignement/réservé (length:2)

            f.seek(startingpoint) # offset 0x2C
            self.record_num=reversebinary(f.read(4))
            
            next_attr_offset=int.from_bytes(self.offset_2_first_attribute) # the first offset to the first attribute

            based_offset=next_attr_offset+offset

            f.seek(next_attr_offset+offset)
            next_attr_type=f.read(4)
            while next_attr_type!=(b'\xFF')*4:
                attr_map=Attribute(f,(next_attr_offset+offset)).attr_mapp
                
                self.Attributes.update(attr_map)


                f.seek(next_attr_offset+offset+4) # length of next attribute

                offset+=next_attr_offset
                next_attr_offset=int.from_bytes(reversebinary(f.read(4)))

                f.seek(next_attr_offset+offset)
                next_attr_type=f.read(4)

            
            attr_type_liste = list(self.Attributes.keys())
            chains_broke=False
            for i in range(0, attr_type_liste.__len__()):
                th_max_offset="0x"+(based_offset+self.Attributes[attr_type_liste[i]]["attr_header"]["length"]).to_bytes(4, 'big', signed=False).hex()
                chains_broke=(
                    chains_broke or ( 
                        self.Attributes[attr_type_liste[i]]["attr_header"]["offset"]!=("0x"+based_offset.to_bytes(4, 'big', signed=False).hex()) or 
                        self.Attributes[attr_type_liste[i]]["attr_header"]["max_offset"]!=th_max_offset
                        )
                    )
                based_offset+=self.Attributes[attr_type_liste[i]]["attr_header"]["length"]
            self.valid_attr_chain= not chains_broke
            
        f.close()


    def getAttributes(self)->dict:
        return self.Attributes
    

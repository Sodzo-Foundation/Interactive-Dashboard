import hashlib,os
import time



"""
Using hashing algorithm to remove duplicate images.
Hashing agorithm: Similar images have the same hash value. So, ensure no two images should have the same hash value.
"""

os.chdir(r'D:\dashboard\images')

#get list of images
file_list = os.listdir()

#define data storages
duplicates = dict()
collected_hash_values = dict()

#initialize counter
count = 1

#implementing the hashing algorithm
for index, filename in  enumerate(os.listdir('.')): #go through the images
    if os.path.isfile(filename):#validate the existance of image
        count += 1
        with open(filename, 'rb') as f: #open image for reading
            image_hash = hashlib.md5(f.read()).hexdigest() #get hash value of the image
        if image_hash not in collected_hash_values: #this hash value not in the collected hash values   
            collected_hash_values[image_hash] = index # update the collected hash values with this hash value, image not duplicate 
        else:  #this hash value is in the collected hash values 
            duplicates[index] = collected_hash_values[image_hash] #update the collected duplicate hash values with this hash value, image is a duplicate.


print("*************Delete duplicates***************")
#remove the duplicate images using their corresponding hashes
for index in duplicates:
    os.remove(file_list[index])

import commands
import re
import sqlite3
import sys

cat_path = sys.argv[1]
photo_uuids = ""
for photo_uuid in sys.argv[2:]:
  if photo_uuids != "":
    photo_uuids += str(", ")
  photo_uuids += "'" + photo_uuid + "'"
query = "select text from Adobe_imageDevelopSettings join Adobe_images on Adobe_imageDevelopSettings.image = Adobe_images.id_local"
if photo_uuids != "":
  query += " where id_global in (" + photo_uuids + ")"

f = open("/Users/conch/hopeful.txt", "w")
conn = sqlite3.connect(cat_path)
db = conn.cursor()
db.execute(query)
for image in db.fetchall():
  f.write(image[0])
  f.write("\n")
f.close()

term_out = commands.getstatusoutput("ps -axo pid,comm | grep '/Applications/Adobe Photoshop Lightroom 4.app/Contents/MacOS/Adobe Photoshop Lightroom 4'")[1]
pid = re.search("(\d+)\s.+", term_out).group(1)
# restart Lightroom
commands.getstatusoutput("kill " + pid)
commands.getstatusoutput("open /Applications/Adobe\ Photoshop\ Lightroom\ 4.app")
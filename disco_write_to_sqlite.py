import commands, re, sqlite3, sys

# close Lightroom
term_out = commands.getstatusoutput("ps -axo pid,comm | grep '/Applications/Adobe Photoshop Lightroom 4.app/Contents/MacOS/Adobe Photoshop Lightroom 4'")[1]
pid = re.search("(\d+)\s.+", term_out).group(1)
commands.getstatusoutput("kill " + pid)

cat_path = sys.argv[1]
photo_uuids = ""
for photo_uuid in sys.argv[2:]:
  if photo_uuids != "":
    photo_uuids += str(", ")
  photo_uuids += "'" + photo_uuid + "'"
query = "select Adobe_images.image, Adobe_imageDevelopSettings.text, Adobe_AdditionalMetadata.xmp from Adobe_imageDevelopSettings join Adobe_images on Adobe_imageDevelopSettings.image = Adobe_images.id_local" +
  " join Adobe_AdditionalMetadata on Adobe_AdditionalMetadata.image = Adobe_images.id_local"
if photo_uuids != "":
  query += " where Adobe_images.id_global in (" + photo_uuids + ")"
query += " order by Adobe_images.captureTime asc"

conn = sqlite3.connect(cat_path)
db = conn.cursor()
db.execute(query)
uq = "update Adobe_imageDevelopSettings set text = '"
with open("/tmp/disco_camera_data.txt", "r") as data:
  for row in db.fetchall():
    d = data.readline()
    d = d[:len(d) - 2] # this is just the angle
    xmp = row[2] # XML that contains the focal length
    focal = int(re.search('exif:FocalLength="(\d+)\/\d+"', xmp).group(1))
    lr = convert_acc_to_lr(d, focal) # need to convert it to the Lightroom slider value
    text = row[1]
    m = re.search("PerspectiveVertical = (.+),", text)
    start = m.start(1)
    end = m.end(1)
    db.execute(uq + text[:start] + lr + text[end:] + "' where image = " + str(row[0]))
conn.commit()
db.close()
conn.close()

# start Lightroom
commands.getstatusoutput("open /Applications/Adobe\ Photoshop\ Lightroom\ 4.app")

def convert_acc_to_lr(angle, focal):
  ratio = 4.26959 - (0.225898 * focal) + (0.00472149 * focal * focal) - (0.000023727 * focal * focal * focal)
  return str(int(round(angle * ratio)))

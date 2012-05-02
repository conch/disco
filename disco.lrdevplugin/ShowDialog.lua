local LrFunctionContext = import 'LrFunctionContext'
local LrDialogs = import 'LrDialogs'
local LrApplication = import 'LrApplication'
local LrTasks = import 'LrTasks'

local function showDialog()
  LrFunctionContext.callWithContext( "showCustomDialog", function( context )
      local action = LrDialogs.confirm("DisCo requires Lightroom to restart.", nil, "Restart")
      if action == "ok" then
        local catalog = LrApplication.activeCatalog()
        local photoUuids = ""
        local photos = catalog:getMultipleSelectedOrAllPhotos()
        for key, value in next, photos, nil do
          photoUuids = photoUuids .. " " .. value:getRawMetadata("uuid")
        end
        LrTasks.execute("python /usr/bin/disco_write_to_sqlite.py " .. catalog:getPath():gsub(" ", "\\ ") .. photoUuids)
      end
  end)
end

LrTasks.startAsyncTask(showDialog)

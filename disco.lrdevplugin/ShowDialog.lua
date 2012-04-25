local LrFunctionContext = import 'LrFunctionContext'
local LrDialogs = import 'LrDialogs'
local LrApplication = import 'LrApplication'
local LrShell = import 'LrShell'

local function showDialog()
  LrFunctionContext.callWithContext( "showCustomDialog", function( context )
      local action = LrDialogs.confirm("DisCo requires Lightroom to restart.", nil, "Restart")
      if action == "ok" then
        LrShell.openPathsViaCommandLine({"/Users/conch/test.py"}, "/usr/bin/python")
      end
  end)
end

import 'LrTasks'.startAsyncTask(showDialog)

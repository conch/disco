return {
  
  LrSdkVersion = 3.0,
  LrSdkMinimumVersion = 1.3, -- minimum SDK version required by this plug-in
  LrToolkitIdentifier = "conch.disco",
  LrPluginName = LOC "$$$/DisCo/PluginName=DisCo",
  LrLibraryMenuItems = {
      {
        title = LOC "$$$/DisCo/CustomDialog=Automatically apply perspective correction on selected images",
        file = "ShowDialog.lua",
    }
  },
  VERSION = { major=3, minor=0, revision=0, build=200000, }
}
function Component()
{
    // default constructor
}

Component.prototype.createOperations = function()
{
    // call default implementation to actually install README.txt!
    component.createOperations();

    if (systemInfo.productType === "windows") {
        component.addOperation(
	    "CreateShortcut",
            "@TargetDir@/win64/pireal.exe",
	    "@DesktopDir@/Pireal.lnk",
            "workingDirectory=@TargetDir@",
	    "iconPath=@TargetDir@/win64/icon.ico",
	    "iconId=0",
	    "description=Open Pireal"
	);
	component.addOperation(
	    "CreateShortcut",
	    "@TargetDir@/win64/pireal.exe",
	    "@StartMenuDir@/Pireal.lnk",
	    "workingDirectory=@TargetDir@",
	    "iconPath=@TargetDir@/win64/icon.ico",
	    "iconId=0",
	    "description=Open README file"
	);
    }
}

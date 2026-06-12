import os

# 修复 package.xml
pkg_xml = r"D:\Android\Sdk\platforms\android-35\package.xml"
with open(pkg_xml, "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ns2:repository xmlns:ns2="http://schemas.android.com/repository/android/common/02"
                 xmlns:ns3="http://schemas.android.com/repository/android/generic/02"
                 xmlns:ns4="http://schemas.android.com/sdk/android/repo/addon2/02"
                 xmlns:ns5="http://schemas.android.com/sdk/android/repo/repository2/03"
                 xmlns:ns6="http://schemas.android.com/sdk/android/repo/sys-img2/03">
    <localPackage path="platforms;android-35" obsolete="false">
        <type-details xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ns5:platformDetailsType">
            <api-level>35</api-level>
            <codename></codename>
            <layoutlib api="15"/>
        </type-details>
        <revision><major>1</major><minor>0</minor><micro>0</micro></revision>
        <display-name>Android SDK Platform 35</display-name>
    </localPackage>
</ns2:repository>
""")
print("Fixed package.xml")

# 修复 source.properties
src_props = r"D:\Android\Sdk\platforms\android-35\source.properties"
with open(src_props, "w", encoding="utf-8") as f:
    f.write("""Pkg.Desc=Android SDK Platform 35
Pkg.UserSrc=false
Pkg.Revision=1
AndroidVersion.ApiLevel=35
Layoutlib.Api=15
Layoutlib.Revision=1
Platform.MinToolsRev=22
""")
print("Fixed source.properties")

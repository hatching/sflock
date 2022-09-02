
/*
Copyright of CybercentreCanada
https://github.com/CybercentreCanada/assemblyline-base/blob/f0d254126c64f73c57b1435f4f66471afdb58811/assemblyline/common/custom.yara#L872:L891
archive/udf
*/

rule archive_udf {

    meta:
        type = "archive/udf"

    strings:
        $ID1 = "CD001"
        $ID2 = "BEA01"
        $ID3 = "NSR02"
        $ID4 = "NSR03"
        $ID5 = "BOOT2"
        $ID6 = "TEA01"

    condition:
        3 of ($ID*) in (0x8000..0x10000)
}

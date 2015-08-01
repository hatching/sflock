# sflock

Sample staging &amp; detonation utility to be used in combination with other
analysis tools.

Birds tend to move around in flocks, therefore the sflock utility can digest a
flock of samples, but also inverse flocks, i.e., samples that contains
numerous sub-samples. As an example, take zip archives.

Simply put, sflock provides a staging area where binary data is investigated
and split into one or more files to be analyzed further by other tools. In
particular sflock focuses on Cuckoo Sandbox.

name = "IntelOpenImageDenoise"

version = "2.3.1"

authors = ["Intel", "Leo Depoix (@piloegao)"]

description = """
    A rez package for the OpenImageDenoise pre-build binaries.
    """

uuid = "com.intel.oidn"

build_command = "python {root}/build.py {install}"


def commands():
    env.OIDN_ROOT.append("{root}/oidn")

    executables = {
        "windows": {
            "oidnBenchmark": "oidnBenchmark.exe",
            "oidnDenoise": "oidnDenoise.exe",
            "oidnTest": "oidnTest.exe",
        },
        "osx": {},
        "linux": {},
    }

    for exec_command, executable_file in executables.get(system.platform).items():
        alias(exec_command, "{root}/bin/%s" % executable_file)
    
    env.PATH.append("{root}/oidn/bin")

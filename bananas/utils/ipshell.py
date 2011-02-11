from IPython.Shell import IPShellEmbed

ipshell = None
try:
    ipshell = IPShellEmbed('', "\nDropping into IPython", "Leaving interpreter")
except:
    pass



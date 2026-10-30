# m-bootloader

`fm1-uboot-1.2.fwsc` is m-bootloader 1.2 by Julius Vitkauskas (MIT, `LICENSE`), from
[github.com/jvitkauskas/m-bootloader](https://github.com/jvitkauskas/m-bootloader), as fm1-base (Charles Vestal) ships
it for Album. The installer can write it after the firmware: hold PLAY while switching on for a recovery menu, or REC
for update mode, even when a firmware won't start. `web/make_site.py` copies it to `firmware/` and puts its SHA-256 in
the installer, which offers it only when the file matches and its identity is FM-1_099.

The option stays hidden until it has been tried on an FM-1 running this firmware: add `?mboot` to the installer's
address to see it.

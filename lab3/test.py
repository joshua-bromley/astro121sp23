import ugradio as ug

ra, dec = ug.coord.sunpos()
print(ra, dec)
ra, dec = ug.coord.precess(ra,dec)
print(ra, dec)
print(ug.coord.get_altaz(ra, dec))
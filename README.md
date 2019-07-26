# PrintShop
## Abstract
Inspired by https://gitlab.com/garrylancaster/pipsta-next/ 

Scripts for using a range of printers, and outputs, from ZX Spectrum Next.  
These scripts are not specifically limited to the Spectrum Next, but the only clients available right now are the Linux NetCat based testing, and the ESP Basic Channel driver.

## To Use
 * Clone this repo
 * Instantiate a VirtualEnv in /server
 * Activate the VirtualEnv
 * Install the requirements
 * Start print-shop.py with the appropriate options

## File Details
| File | Use |
| ------ | ------ |
| server/print-shop.py | Listens on port 65432 and outputs data received printer after a number of optional converstions. Compatble with Garry's original, linked above|
| server/printers | Individual printer driver modules
| tests/ | Shell scripts to test the drivers from Linux

#import sys
#import bluetooth
import aioble
import uasyncio as asyncio
from micropython import const
import time
# Define the Beacon UUID and Company ID 
BEACON_UUID = const(0xFEAA)  # Example Eddystone UUID (Google's beacon format)
COMPANY_ID = const(0x004C)   # Example Apple company ID for iBeacon
name = 'DataMann00185'
async def scan_for_beacons():
    print("Starting BLE beacon scan...")
    
    
    #async with aioble.scan(timeout=10) as scanner:
    async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            
            print("Device Name",result.name())
            #print(f"Found BLE device: {result.device.addr}")
            #print(f"RSSI: {result.rssi}")
            mfdId = result.manufacturer()
            print("Manufacturer data:", mfdId)
            #print("Services ",result.services())
            time.sleep(1)
            """if BEACON_UUID in result.services:
                print("Beacon UUID found:", BEACON_UUID)
            if COMPANY_ID in result.manufacturer:
                print("Manufacturer ID found:", COMPANY_ID)
                print("Manufacturer data:", result.manufacturer[COMPANY_ID])"""
            

async def main():
    while True:
        await scan_for_beacons()
        await asyncio.sleep(2)  

asyncio.run(main())


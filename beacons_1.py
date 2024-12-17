import aioble
import uasyncio as asyncio
import struct
import json

# Define the Company ID for Apple iBeacon
COMPANY_ID = 0x004C  # Apple Company ID for iBeacon (in decimal: 76)

f = open('config.json',"r")
config = json.load(f)

# Function to scan for BLE devices
async def scan_for_beacons():
    print("Starting BLE beacon scan...")

    # Start scanning for BLE devices
    async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
    #async with aioble.scan(timeout=10) as scanner:
        async for result in scanner:
            # Print the address (MAC address) and RSSI of the BLE device
            print(f"Found BLE device: {result.device.addr.hex()}")
            print(f"RSSI: {result.rssi}")

            # Print name if available
            if result.name():
                print(f"Device Name: {result.name()}")

            # Manufacturer data is expected in the BLE advertisement
            manufacturer_data = list(result.manufacturer())  # Convert generator to list
            if manufacturer_data:
                print(f"Manufacturer Data: {manufacturer_data}")

                # Check for iBeacon Manufacturer Data
                for company_id, data in manufacturer_data:
                    print(f"Company ID: {company_id}")
                    print(f"Raw Manufacturer Data: {data}")
                    mfd_id = company_id
                    if mfd_id == config['BLE_Beacon']['MFD_ID']:
                        print("Manufacturer Id ",hex(mfd_id))
                        # Ensure the data length is sufficient and it starts with the iBeacon prefix (0x02 0x15)
                        if len(data) >= 25 and data[:2] == b'\x02\x15':
                            # Parse the iBeacon UUID, Major, Minor, and TX Power
                            uuid = data[2:18]  # 16 bytes
                            major, minor, tx_power = struct.unpack('>HHb', data[18:25])

                            print(f"iBeacon detected:")
                            print(f"  UUID: {uuid.hex()}")
                            print(f"  Major: {major}")
                            print(f"  Minor: {minor}")
                            print(f"  TX Power: {tx_power}")
                        else:
                            print("Manufacturer data found, but no valid iBeacon prefix detected.")
            else:
                print("No Manufacturer Data found.")

# Main function to run the scanning task
async def main():
    while True:
        await scan_for_beacons()
        await asyncio.sleep(2)  # Delay between scans

# Run the event loop
asyncio.run(main())


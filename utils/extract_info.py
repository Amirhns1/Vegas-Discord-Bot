def extract_message_info(message):
    content = message.content.splitlines()
    health_value = None
    player_name = None
    plate_number = None
    car_status = "out"

    for line in content:
        if line.startswith("Gozashtan"):
            car_status = "in"
        if line.startswith("Health"):
            try:
                health_value = int(line.split(":")[1].strip().replace("%", ""))
            except:
                pass
        if line.startswith("Plate"):
            plate_number = line.split(":")[1].strip()
        if line.startswith("steam:"):
            parts = line.split()
            if len(parts) >= 2:
                player_name = parts[1].strip()

    return health_value, player_name, plate_number, car_status

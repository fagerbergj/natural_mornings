# While true
    # Pull config from files
    # Parse config into array
    # get current day config
    # if day is enabled
        # if light activated is true
            # read light sensor for 1 minuet
            # average result to set triggered to true or not
        # else
            # sleep 1 minuet
            # check to see if current time = time from config
        # if system is triggered
            # if sound
                # play sound
            # if window
                # move motor
            # if blinds
                # move motor

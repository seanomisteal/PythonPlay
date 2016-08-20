import plistlib


def main():
    # findDuplicates("test-data\maya.xml")
    filenames = ("test-data\pl1.xml", "test-data\pl2.xml")
    findCommonTracks(filenames)

def findCommonTracks(filenames):
    trackNameSets = []
    for filename in filenames:
        trackNames = set()
        plist = plistlib.readPlist(filename)
        tracks = plist["Tracks"]
        for trackId, track in tracks.items():
            try:
                trackNames.add(track['Name'])
            except:
                pass
        trackNameSets.append(trackNames)

        # get the set of common tracks
        commonTracks = set.intersection(*trackNameSets)

        # write to file 
        if len(commonTracks) > 0:
            f = open("common.txt", "w")
            for val in commonTracks:
                s = "%s\n" % val
                f.write(s.encode("UTF-8"))
            f.close()
            print("%d common tracks found" % len(commonTracks))
        else:
            print("No common tracks!")

def findDuplicates(filename):
    print('Finding duplicate tracks in %s...' % filename)
    # read in a playlist
    plist = plistlib.readPlist(filename)
    # get the tracks from the Tracks dictionary
    tracks = plist['Tracks']
    # create a track name dictionary
    trackNames = {}
    # iterate through the tracks
    for trackId, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            # look for existing entries
            if name in trackNames:
                if duration//1000 == trackNames[name][0]//1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count+1)
            else:
                # add dictionary entry as tuple (duration, count)
                trackNames[name] = (duration,1)
        except:
            # ignore
            pass

    dups = []
    for k, v in trackNames.items():
        if v[1] > 1:
            dups.append((v[1], k))
    # save duplicates to a file 
    if len(dups) > 0:
        print("Found %d duplicates. Track names saved to dup.txt" % len(dups))
    else:
        print("No duplicate tracks found!")
    f = open("dups.txt", "w")
    for val in dups:
        f.write("[%d] %s\n" % (val[0], val[1]))
    f.close()

# main method
if __name__ == '__main__':
    main()

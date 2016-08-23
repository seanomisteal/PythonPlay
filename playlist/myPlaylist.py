import plistlib


def main():
    filename = "test-data\maya.xml"
    #findDuplicates(filename)
    #filenames = ("test-data\pl1.xml", "test-data\pl2.xml")
    #findCommonTracks(filenames)
    filename = "test-data\mymusic.xml"
    plotStats(filename)

def plotStats(filename):
    # read in a playlist
    plist = plistlib.readPlist(filename)
    # get the tracks from the playlist
    tracks = plist['Tracks']
    # create list of song ratings and track durations
    ratings = []
    durations = []
    # iterate through the tracks
    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            pass
    # ensure that valid data was collected 
    if ratings == [] or durations == []:
        print("No valid Album Rating/Duration data in %s." % filename)
        return

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
        f = open("common.txt", "wb")
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

            if (name, duration//1000) in trackNames:
                count = trackNames[(name, duration//1000)]
                trackNames[(name, duration//1000)] = count+1
            else:
                trackNames[(name, duration//1000)] = 1
        except:
            pass

    dups = []
    for k, v in trackNames.items():
        if v > 1:
            dups.append((v, k))
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

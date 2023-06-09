# ALl headers

S_HEADER = [
    'line',       # line ID. Stationen mit gleicher ID werden gestapelt oder selektiert
    'point',        # Stationen mit gleicher point ID werden gestapelt oder selektiert
    'index',        # identifiziert wiederholte Nutzung einer Quelle
    'easting',
    'northing',
    'elevation',
    'depth',
    'code',         # Kennzeichnung von Anregungs- oder Empfänger
    'uht',          # Aufzeit (uphole time) an einer Spregseismik-Quelle
    'waterdepth',   # Wassertiefe an der Station
    'stat',         # Stations-spezifische statische Korrektur
    'srd',          # Bezugsniveau
    'day',
    'hour',
    'min',
    'sec',
    'patch',        # Nummer, welche die Rotation (vorlaufende Verlegung) von Geophone beschreibt
    'ts',           # Kopie Zeit in Sekungen ab Jahresbeginn
    'spare1',
    'spare2'
]
R_HEADER = [
    'line',
    'point',
    'index',
    'easting',
    'northing',
    'elevation',
    'depth',
    'code',
    'uht',
    'waterdep',
    'srd',
    'patch',
    'ts',
    'spare1',
    'spare2'
]
X_HEADER = [
    'ffid',         # record number
    'sline',        # source line
    'spoint',       # source point
    'sindex',       # source index
    'nChan',        # Anzahl aktiver kanäle bei der Aufzeichnung
    'CHAN',         # Kanal-IDs
    'rline',        # receiver line IDs pro Kanal
    'rpoint',       # receiver point IDs pro Kanal
    'rindex',       # receiver index pro Kanal
    'time',         # Zeitmarke der FFID
    'instr',        # Instrument Code
    'ksrc',         # Index des SPS-S Datensatz zum SPS-X Datensatz
    'krec'          # Indices der SPS-R Datensätze zum SPS-X datensatz
]
BINARY_FILE_HEADER = [
    [4, 'jobid', False],  # Job identification number
    [4, 'nline', False],  # Line number
    [4, 'nreel', False],  # Reel number
    [2, 'ntr', True],  # Number of data traces per ensemble
    [2, 'naux', True],  # Number of auxiliary traces per ensemble
    [2, 'sint', False],  # Sample interval
    [2, 'sintori', False],  # Sample interval of original field recording
    [2, 'nsam', False],  # Number of sample per data trace
    [2, 'nsamor', False],  # Number of sample per data trace for original field recording
    [2, 'dform', True],  # Data sample format code. 1= 4-byte IMB floating point
    [2, 'fold', False],  # Ensemble fold
    [2, 'trsort', False],  # Trace sorting code
    [2, 'vstk', False],  # Vertical sum code
    [2, 'swfst', False],  # Sweep frequency at start (Hz)
    [2, 'swfend', False],  # Sweep frequency at end (Hz)
    [2, 'swl', False],  # Sweep length (ms)
    [2, 'swtyp', False],  # Sweep type code
    [2, 'nswchan', False],  # Trace number of sweep channels
    [2, 'swtaplst', False],  # Sweep trace taper length start (ms)
    [2, 'swtaplend', False],  # Sweep trace taper length end (ms)
    [2, 'taptyp', False],  # Taper type
    [2, 'corrtr', False],  # Correlated data traces
    [2, 'bgain', False],  # Binary gain recovered
    [2, 'again', False],  # Amplitude recovery method
    [2, 'meassys', False],  # Measurement system, 1=meters 2=feets
    [2, 'ipolar', False],  # Impulse signal polarity
    [2, 'vpolar', False],  # Vibratory polarity code
    [4, 'exntr', False],  # Extended number of data traces per ensemble
    [4, 'exnaux', False],  # Extended number of auxiliary traces per ensemble
    [7, 'exnsint', False],  # Extended sample interval
    [7, 'exnsintori', False],  # Extended sample interval of original field recording
    [4, 'exns', False],  # Extended number of sample per data trace in original record
    [4, 'exnef', False],  # Extended ensemble fold
    [4, 'endia', False],  # integer constant for endinaness #TODO : 3297-3300 -> extract endinnaess
    [200, 'una', False],  # Unassigned
    [1, 'majrevn', True],  # Major segy format revision number (3501)
    [1, 'minrevn', True],  # Minor segy format revision number
    [2, 'fixlflag', True],  # Fixed length trace flag
    [2, 'nbyteext', False],  # Number of 3200-byte extended textual file header
    [4, 'naddbyt', False],  # Maximum number of additional 240 byte trace headers
    [2, 'tcode', False],  # Time basis code
    [8, 'ntrfil', False],  # Number of trace in file or stream
    [8, 'byoff', False],  # Byte offset of first trace realtive to start of file or stream
    [4, 'nstanz', False],  # Number of 3200 byte data trailer stanza records following last trace
    [8, 'una', False],  # Unassigned 2
]

# TODO : modify trace header according to : https://wiki.seismic-unix.org/sudoc:su_data_format
TRACE_HEADER = [
    [4, 'tracl'],  # Trace sequence number within line
    [4, 'tracr'],  # Trace sequence number within segy file
    [4, 'fldr'],  # Original field record number
    [4, 'tracf'],  # Trace number within original field record (=tracf)
    [4, 'ep'],  # Energy source point number
    [4, 'cdp'],  # Ensemble number
    [4, 'cdpt'],  # Number trace within ensemble
    [2, 'trid'],  # Trace identification code
    [2, 'nvs'],  # Number of vertically summed traces yielding this trace
    [2, 'nhs'],  # Number of horizontally summed traces yielding this trace
    [2, 'duse'],  # Data use, 1=production 0=test
    [4, 'offset'],  # Distance from center source to center receiver group
    [4, 'gelev'],  # Elevation of receiver group
    [4, 'selev'],  # Surface elevation at source location
    [4, 'sdepth'],  # Source depth below surface
    [4, 'gdel'],  # Seismic datum elevation at receiver group
    [4, 'sdel'],  # Seismic datum elevation at source
    [4, 'swdep'],  # Water column height at source location
    [4, 'gwdep'],  # Water column height at receiver location
    [2, 'scalel'],  # Scalar to be applied to elevations and depth prior writhing into tr header
    [2, 'scalco'],  # Scalar to be applied to coordinates
    [4, 'sx'],  # Source coordinate x, easting
    [4, 'sy'],  # Source coordinate y, northing
    [4, 'gx'],  # Group coordinate x, easting
    [4, 'gy'],  # Group coordinate y, northing
    [2, 'counit'],  # Coordinate units
    [2, 'wevel'],  # Weathering velocity (m/s or ft/s)
    [2, 'swevel'],  # Subweathering velocity (m/s or ft/s)
    [2, 'sut'],  # Uphole time at source in ms
    [2, 'gut'],  # Uphole time at group in ms
    [2, 'sstat'],  # Source static correction in ms
    [2, 'gstat'],  # Group static correction in ms
    [2, 'tstat'],  # Total static applied in ms
    [2, 'laga'],  # Lag time A in ms. Time between time break and end header.
    [2, 'lagb'],  # Lag time B in ms. Time between time break and initiation time of energy source.
    [2, 'delrt'],  # Delay recording time. Between initiation time source and time recording samples.
    [2, 'muts'],  # Mute time. Start time in ms
    [2, 'mute'],  # Mute time. End time in ms
    [2, 'ns'],  # Number of sample of this trace
    [2, 'dt'],  # Sample interval for this trace. in microseconds for t, Hz for f, m/ft for depth
    [2, 'gain'],  # Gain type
    [2, 'igc'],  # Instrument gain constant (dB)
    [2, 'igi'],  # Instrument early or initial gain (dB)
    [2, 'corr'],  # Correlated. 1=no, 0=yes
    [2, 'sfs'],  # Sweep frequency at start (Hz)
    [2, 'sfe'],  # Sweep frequency at end (Hz)
    [2, 'slen'],  # Sweep length (ms)
    [2, 'styp'],  # Sweep type code
    [2, 'stas'],  # Sweep trace taper length start (ms)
    [2, 'stae'],  # Sweep trace taper length end (ms)
    [2, 'tatyp'],  # Taper type. 1=linear, 2=cos, 3=other
    [2, 'afilf'],  # Frequency alias filter (Hz)
    [2, 'afils'],  # Slope alias filter (dB/octave)
    [2, 'nofilf'],  # Notch filter frequency (Hz)
    [2, 'nofils'],  # Notch filter slope (dB/octave)
    [2, 'lcf'],  # Low-cut frequency (Hz)
    [2, 'hcf'],  # High-cut frequency (Hz)
    [2, 'lcs'],  # Low-cut slope (dB/octave)
    [2, 'hcs'],  # High-cut slope (dB/octave)
    [2, 'year'],  # Year data recorded
    [2, 'day'],  # Day of year
    [2, 'hour'],  # Hour of day
    [2, 'minute'],  # Minute of hour
    [2, 'sec'],  # Second of minute
    [2, 'timbas'],  # Time basis code
    [2, 'trwf'],  # Trace weighting factor
    [2, 'grnors'],  # Geophone group number of roll switch position one
    [2, 'grnofr'],  # Geophone group number of trace number one within original field record
    [2, 'grnlof'],  # Geophone group number of last trace within original field record
    [2, 'gaps'],  # Gap size, number of groups dropped
    [2, 'ofrav'],  # Over travel associated with taper. 1=down/behind, 2=up/ahead
    [4, 'cdpx'],  # X coordinate of ensemble (CDP) position of this trace
    [4, 'cdpy'],  # Y coordinate of ensemble (CDP) position of this trace
    [4, 'ninline'],  # In-line number for 3D
    [4, 'ncrline'],  # Cross-line number for 3D
    [4, 'spoint'],  # Shotpoint number
    [2, 'spsc'],  # Scalar to be applied to shotpoint number
    [2, 'trunit'],  # Trace value measurement unit
    [6, 'transc'],  # Transduction constant
    [2, 'transunit'],  # Transduction units
    [2, 'devid'],  # Device/trace identifier: 4368 vibrator, 20316 gun
    [2, 'tsc'],  # Scalar to be applied on time
    [2, 'styp'],  # Source type / orientation
    [6, 'senerd'],  # Source energy direction
    [6, 'smeas'],  # Source measurement
    [2, 'smeasunit'],  # Source measurement unit
    [8, 'trheadnam'],  # Trace header name. Ascii or ebcdic text.
]

EXTENDED_HEADER = [[8, str(n)] for n in range(int(240 / 8))]

PROPRIETARY_HEADER = [
    [232, 'user'],
    [8, 'extension name']
]

TRACE_HEADER_ADDITIONAL = [
    [4, 'sline'],  # Source line number
    [4, 'spoint'],  # Source point number on line
    [4, 'sindex'],  # Source index
    [4, 'rline'],  # Receiver line
    [4, 'rpoint'],  # Receiver point number on line
    [4, 'rindex'],  # Receiver station index
    [4, 'azim'],  # Source-to-receiver azimuth (deg)
    [4, 'dip'],  # Source-to-receiver dip (deg). Negative -> source above receiver
    [4, 'spskx'],  # Index of corresponding SPS-X record
    [4, 'spsks'],  # Index of corresponding SPS-S record
    [4, 'spskr'],  # Index of corresponding SPS-R record
    # added for snavmergesps
    [4, 'ssp1'],   # spare in snavmergesps
    [4, 'ssp2'],   # spare in snavmergesps
]
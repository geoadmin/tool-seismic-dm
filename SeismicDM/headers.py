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

# trace header according to : https://wiki.seismic-unix.org/sudoc:su_data_format
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

## OBSPY trace headers
STH_keys = [u'trace_sequence_number_within_line',
                        u'trace_sequence_number_within_segy_file',
                        u'scalar_to_be_applied_to_all_coordinates',
                        u'source_coordinate_x',
                        u'source_coordinate_y',
                        u'group_coordinate_x',
                        u'group_coordinate_y',
                        u'coordinate_units',
                        u'lag_time_A',
                        u'lag_time_B',
                        u'delay_recording_time',
                        u'number_of_samples_in_this_trace',
                        u'sample_interval_in_ms_for_this_trace',
                        u'x_coordinate_of_ensemble_position_of_this_trace',
                        u'y_coordinate_of_ensemble_position_of_this_trace',
                        u'for_3d_poststack_data_this_field_is_for_in_line_number',
                        u'for_3d_poststack_data_this_field_is_for_cross_line_number']

#: The format of the 400 byte long binary file header.
BINARY_FILE_HEADER_FORMAT = [
    # [length, name, mandatory]
    [4, 'job_identification_number', False],
    [4, 'line_number', False],
    [4, 'reel_number', False],
    [2, 'number_of_data_traces_per_ensemble', False],
    [2, 'number_of_auxiliary_traces_per_ensemble', False],
    [2, 'sample_interval_in_microseconds', True],
    [2, 'sample_interval_in_microseconds_of_original_field_recording', False],
    [2, 'number_of_samples_per_data_trace', True],
    [2, 'number_of_samples_per_data_trace_for_original_field_recording',
     False],
    [2, 'data_sample_format_code', True],
    [2, 'ensemble_fold', False],
    [2, 'trace_sorting_code', False],
    [2, 'vertical_sum_code', False],
    [2, 'sweep_frequency_at_start', False],
    [2, 'sweep_frequency_at_end', False],
    [2, 'sweep_length', False],
    [2, 'sweep_type_code', False],
    [2, 'trace_number_of_sweep_channel', False],
    [2, 'sweep_trace_taper_length_in_ms_at_start', False],
    [2, 'sweep_trace_taper_length_in_ms_at_end', False],
    [2, 'taper_type', False],
    [2, 'correlated_data_traces', False],
    [2, 'binary_gain_recovered', False],
    [2, 'amplitude_recovery_method', False],
    [2, 'measurement_system', False],
    [2, 'impulse_signal_polarity', False],
    [2, 'vibratory_polarity_code', False],
    [240, 'unassigned_1', False],
    [2, 'seg_y_format_revision_number', True],
    [2, 'fixed_length_trace_flag', True],
    [2, 'number_of_3200_byte_ext_file_header_records_following', True],
    [94, 'unassigned_2', False]] #u.nassigned_2

#: The format of the 240 byte long trace header.
TRACE_HEADER_FORMAT = [
    # [length, name, special_type, start_byte]
    # Special type enforces a different format while unpacking using struct.
    [4, 'trace_sequence_number_within_line', False, 0],
    [4, 'trace_sequence_number_within_segy_file', False, 4],
    [4, 'original_field_record_number', False, 8],
    [4, 'trace_number_within_the_original_field_record', False, 12],
    [4, 'energy_source_point_number', False, 16],
    [4, 'ensemble_number', False, 20],
    [4, 'trace_number_within_the_ensemble', False, 24],
    [2, 'trace_identification_code', False, 28],
    [2, 'number_of_vertically_summed_traces_yielding_this_trace', False, 30],
    [2, 'number_of_horizontally_stacked_traces_yielding_this_trace', False,
     32],
    [2, 'data_use', False, 34],
    [4, 'distance_from_center_of_the_source_point_to_' +
     'the_center_of_the_receiver_group', False, 36],
    [4, 'receiver_group_elevation', False, 40],
    [4, 'surface_elevation_at_source', False, 44],
    [4, 'source_depth_below_surface', False, 48],
    [4, 'datum_elevation_at_receiver_group', False, 52],
    [4, 'datum_elevation_at_source', False, 56],
    [4, 'water_depth_at_source', False, 60],
    [4, 'water_depth_at_group', False, 64],
    [2, 'scalar_to_be_applied_to_all_elevations_and_depths', False, 68],
    [2, 'scalar_to_be_applied_to_all_coordinates', False, 70],
    [4, 'source_coordinate_x', False, 72],
    [4, 'source_coordinate_y', False, 76],
    [4, 'group_coordinate_x', False, 80],
    [4, 'group_coordinate_y', False, 84],
    [2, 'coordinate_units', False, 88],
    [2, 'weathering_velocity', False, 90],
    [2, 'subweathering_velocity', False, 92],
    [2, 'uphole_time_at_source_in_ms', False, 94],
    [2, 'uphole_time_at_group_in_ms', False, 96],
    [2, 'source_static_correction_in_ms', False, 98],
    [2, 'group_static_correction_in_ms', False, 100],
    [2, 'total_static_applied_in_ms', False, 102],
    [2, 'lag_time_A', False, 104],
    [2, 'lag_time_B', False, 106],
    [2, 'delay_recording_time', False, 108],
    [2, 'mute_time_start_time_in_ms', False, 110],
    [2, 'mute_time_end_time_in_ms', False, 112],
    [2, 'number_of_samples_in_this_trace', 'H', 114],
    [2, 'sample_interval_in_ms_for_this_trace', 'H', 116],
    [2, 'gain_type_of_field_instruments', False, 118],
    [2, 'instrument_gain_constant', False, 120],
    [2, 'instrument_early_or_initial_gain', False, 122],
    [2, 'correlated', False, 124],
    [2, 'sweep_frequency_at_start', False, 126],
    [2, 'sweep_frequency_at_end', False, 128],
    [2, 'sweep_length_in_ms', False, 130],
    [2, 'sweep_type', False, 132],
    [2, 'sweep_trace_taper_length_at_start_in_ms', False, 134],
    [2, 'sweep_trace_taper_length_at_end_in_ms', False, 136],
    [2, 'taper_type', False, 138],
    [2, 'alias_filter_frequency', False, 140],
    [2, 'alias_filter_slope', False, 142],
    [2, 'notch_filter_frequency', False, 144],
    [2, 'notch_filter_slope', False, 146],
    [2, 'low_cut_frequency', False, 148],
    [2, 'high_cut_frequency', False, 150],
    [2, 'low_cut_slope', False, 152],
    [2, 'high_cut_slope', False, 154],
    [2, 'year_data_recorded', False, 156],
    [2, 'day_of_year', False, 158],
    [2, 'hour_of_day', False, 160],
    [2, 'minute_of_hour', False, 162],
    [2, 'second_of_minute', False, 164],
    [2, 'time_basis_code', False, 166],
    [2, 'trace_weighting_factor', False, 168],
    [2, 'geophone_group_number_of_roll_switch_position_one', False, 170],
    [2, 'geophone_group_number_of_trace_number_one', False, 172],
    [2, 'geophone_group_number_of_last_trace', False, 174],
    [2, 'gap_size', False, 176],
    [2, 'over_travel_associated_with_taper', False, 178],
    [4, 'x_coordinate_of_ensemble_position_of_this_trace', False, 180],
    [4, 'y_coordinate_of_ensemble_position_of_this_trace', False, 184],
    [4, 'for_3d_poststack_data_this_field_is_for_in_line_number', False, 188],
    [4, 'for_3d_poststack_data_this_field_is_for_cross_line_number', False,
     192],
    [4, 'shotpoint_number', False, 196],
    [2, 'scalar_to_be_applied_to_the_shotpoint_number', False, 200],
    [2, 'trace_value_measurement_unit', False, 202],
    # The transduction constant is encoded with the mantissa and the power of
    # the exponent, e.g.:
    # transduction_constant =
    # transduction_constant_mantissa * 10 ** transduction_constant_exponent
    [4, 'transduction_constant_mantissa', False, 204],
    [2, 'transduction_constant_exponent', False, 208],
    [2, 'transduction_units', False, 210],
    [2, 'device_trace_identifier', False, 212],
    [2, 'scalar_to_be_applied_to_times', False, 214],
    [2, 'source_type_orientation', False, 216],
    # XXX: In the SEGY manual it is unclear how the source energy direction
    # with respect to the source orientation is actually defined. It has 6
    # bytes but it seems like it would just need 4. It is encoded as tenths of
    # degrees, e.g. 347.8 is encoded as 3478.
    # As I am totally unclear how this relates to the 6 byte long field I
    # assume that the source energy direction is also encoded as the mantissa
    # and the power of the exponent, e.g.: source_energy_direction =
    # source_energy_direction_mantissa * 10 ** source_energy_direction_exponent
    # Any clarification on the subject is very welcome.
    [4, 'source_energy_direction_mantissa', False, 218],
    [2, 'source_energy_direction_exponent', False, 222],
    # The source measurement is encoded with the mantissa and the power of
    # the exponent, e.g.:
    # source_measurement =
    # source_measurement_mantissa * 10 ** source_measurement_exponent
    [4, 'source_measurement_mantissa', False, 224],
    [2, 'source_measurement_exponent', False, 228],
    [2, 'source_measurement_unit', False, 230],
    [8, 'unassigned', False, 232]]
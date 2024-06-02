class CholecT50StaticVariables(object):
    instrument_information_dict = {
        '0': {
            'name': 'grasper',
            'colour': [0,0,255]     
            },
        '1': {
            'name': 'bipolar',
            'colour': [0,255,0] 
        },
        '2': {
            'name': 'hook',
            'colour': [255,0,0] 
        },
        '3': {
            'name': 'scissors',
            'colour': [255,0,255] 
        },
        '4': {
            'name': 'clipper',
            'colour': [0,255,255] 
        },
        '5': {
            'name': 'irrigator',
            'colour': [255,255,0] 
        },
        '6': {
            'name': 'background',
            'colour': [0,0,0] 
        }
    }

    bbox_format = 'topleft_width_height'

    bbox_value_style='relative'

    background_id=6 

class CholecSeg8kStaticVariables(object):
    class_information_dict = {
            '0': {
                'name': 'Black Background',
                'colour': 50, #505050,
                'type': 'background'
                },
            '1': {
                'name': 'Abdominal Wall',
                'colour': 11, #111111 
                'type': 'anatomy'
            },
            '2': {
                'name': 'Liver',
                'colour': 21, #212121 
                'type': 'anatomy'
            },
            '3': {
                'name': 'Gastrointestinal Tract',
                'colour': 13,  #131313
                'type': 'anatomy'
            },
            '4': {
                'name': 'Fat',
                'colour': 12, #121212
                'type': 'anatomy'
            },
            '5': {
                'name': 'Grasper',
                'colour': 31,  #313131
                'type': 'instrument'
            },
            '6': {
                'name': 'Connective Tissue',
                'colour': 23,  #232323
                'type': 'anatomy'
            },
            '7': {
                'name': 'Blood',
                'colour': 24,  #242424
                'type': 'anatomy'
            },
            '8': {
                'name': 'Cystic Duct',
                'colour': 25,  #252525
                'type': 'anatomy'
            },
            '9': {
                'name': 'L-hook Electrocautery',
                'colour': 32, #323232
                'type': 'instrument'
            },
            '10': {
                'name': 'Gallbladder',
                'colour': 22,  #222222
                'type': 'anatomy'
            },
            '11': {
                'name': 'Hepatic Vein',
                'colour': 33, #333333
                'type': 'anatomy'
            },
            '12': {
                'name': 'Liver Ligament',
                'colour': 5, #050505
                'type': 'anatomy'
            }
        }

class CholecInstanceSegVariables(object):    
    
    instrument_id_to_instrument_class_dict = {
        '1': 'grasper',
        '2': 'hook',
        '3': 'irrigator',
        '4': 'clipper',
        '5': 'bipolar',
        '6': 'scissors',
        '7': 'snare' 
    }

    background_id = 0
    
    dataset_size = 39078
    
    seq_to_split_dict = {
        'VID09_seg8k': 'test',
        'VID14_t50_full': 'test',
        'VID15_t50_full': 'test',
        'VID20_seg8k': 'test',
        'VID22_t50_full': 'test',
        'VID24_seg8k': 'test',
        'VID29_t50_full': 'test',
        'VID55_seg8k': 'test',
        'VID01_seg8k': 'train',
        'VID01_t50_full': 'train',
        'VID02_t50_sparse': 'train',
        'VID04_t50_sparse': 'train',
        'VID05_t50_sparse': 'train',
        'VID06_t50_sparse': 'train',
        'VID08_t50_sparse': 'train',
        'VID103_t50_sparse': 'train',
        'VID10_t50_sparse': 'train',
        'VID110_t50_sparse': 'train',
        'VID111_t50_sparse': 'train',
        'VID12_seg8k': 'train',
        'VID12_t50_full': 'train',
        'VID13_t50_sparse': 'train',
        'VID18_seg8k': 'train',
        'VID18_t50_full': 'train',
        'VID25_seg8k': 'train',
        'VID25_t50_full': 'train',
        'VID26_seg8k': 'train',
        'VID26_t50_full': 'train',
        'VID27_seg8k': 'train',
        'VID27_t50_full': 'train',
        'VID31_t50_sparse': 'train',
        'VID32_t50_sparse': 'train',
        'VID35_seg8k': 'train',
        'VID35_t50_full': 'train',
        'VID36_t50_sparse': 'train',
        'VID40_t50_sparse': 'train',
        'VID42_t50_sparse': 'train',
        'VID43_seg8k': 'train',
        'VID43_t50_full': 'train',
        'VID47_t50_sparse': 'train',
        'VID48_seg8k': 'train',
        'VID48_t50_full': 'train',
        'VID49_t50_sparse': 'train',
        'VID50_t50_sparse': 'train',
        'VID51_t50_sparse': 'train',
        'VID52_seg8k': 'train',
        'VID52_t50_full': 'train',
        'VID56_t50_sparse': 'train',
        'VID57_t50_sparse': 'train',
        'VID60_t50_sparse': 'train',
        'VID62_t50_sparse': 'train',
        'VID65_t50_sparse': 'train',
        'VID66_t50_sparse': 'train',
        'VID68_t50_sparse': 'train',
        'VID70_t50_sparse': 'train',
        'VID73_t50_sparse': 'train',
        'VID74_t50_sparse': 'train',
        'VID75_t50_sparse': 'train',
        'VID78_t50_sparse': 'train',
        'VID79_t50_sparse': 'train',
        'VID80_t50_sparse': 'train',
        'VID92_t50_sparse': 'train',
        'VID96_t50_sparse': 'train',
        'VID17_seg8k': 'val',
        'VID23_t50_full': 'val',
        'VID28_seg8k': 'val',
        'VID37_seg8k': 'val',
        'VID03_t80_sparse':	'val',
        'VID07_t80_sparse':	'test',
        'VID11_t80_sparse':	'val',
        'VID16_t80_sparse':	'test',
        'VID19_t80_sparse':	'val',
        'VID21_t80_sparse':	'test',
        'VID30_t80_sparse':	'val',
        'VID33_t80_sparse':	'test',
        'VID34_t80_sparse':	'val',
        'VID38_t80_sparse':	'test',
        'VID39_t80_sparse':	'val',
        'VID41_t80_sparse':	'test',
        'VID44_t80_sparse':	'val',
        'VID45_t80_sparse':	'test',
        'VID46_t80_sparse':	'val',
        'VID53_t80_sparse':	'test',
        'VID54_t80_sparse':	'val',
        'VID58_t80_sparse':	'test',
        'VID59_t80_sparse':	'val',
        'VID61_t80_sparse':	'test',
        'VID63_t80_sparse':	'val',
        'VID64_t80_sparse':	'test',
        'VID67_t80_sparse':	'val',
        'VID69_t80_sparse':	'test',
        'VID71_t80_sparse':	'val',
        'VID72_t80_sparse':	'test',
        'VID76_t80_sparse':	'val',
        'VID77_t80_sparse':	'test',    
        }

    
   


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

    
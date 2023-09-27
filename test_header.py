import unittest
from os import path

THIS_DIR = path.dirname( path.realpath( __file__ ) )
ASSET_DIR = path.join( THIS_DIR, 'assets' )
TEST_DIR = path.join( ASSET_DIR, 'test', 'interface' )

def get_asset_path( name, ext = '.png' ):
	return path.join( TEST_DIR, name + ext )
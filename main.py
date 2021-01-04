import json
import os
import shutil
import sys

from PIL import Image

texture_size = None


def flush_image(path):
    img = Image.open(os.path.join('assets', 'flushed.png'))
    background = Image.open(path)

    if texture_size is None:
        image_size = background.size
    else:
        image_size = texture_size

    if img.size != texture_size:
        img = img.resize(image_size, Image.ANTIALIAS)

    if background.size != texture_size:
        background = background.resize(image_size, Image.NONE)

    background.paste(img, (0, 0), img)
    background.save(path, 'PNG')


def flush_directory(path):
    for image in os.listdir(path):
        if image.endswith('.png'):
            flush_image(os.path.join(path, image))
    return


if __name__ == '__main__':
    zip_file = sys.argv[1]
    if len(sys.argv) > 2:
        size = int(sys.argv[2])
        texture_size = (size, size)
    zip_dest = zip_file[:-4]
    print('Unzipping pack')
    shutil.unpack_archive(zip_file, zip_dest)

    print('Flushing pack description')
    meta_file = os.path.join(zip_dest, 'pack.mcmeta')
    with open(meta_file, 'r') as f:
        pack = json.load(f)
    desc = pack['pack']['description']
    pack['pack']['description'] = '[Flushed] %s' % desc
    with open(meta_file, 'w') as f:
        json.dump(pack, f)

    print('Flushing pack image')
    flush_image(os.path.join(zip_dest, 'pack.png'))

    if pack['pack']['pack_format'] > 3:
        print('Flushing block textures')
        flush_directory(os.path.join(zip_dest, 'assets', 'minecraft', 'textures', 'block'))
        print('Flushing item textures')
        flush_directory(os.path.join(zip_dest, 'assets', 'minecraft', 'textures', 'item'))
    else:
        print('Flushing block textures')
        flush_directory(os.path.join(zip_dest, 'assets', 'minecraft', 'textures', 'blocks'))
        print('Flushing item textures')
        flush_directory(os.path.join(zip_dest, 'assets', 'minecraft', 'textures', 'items'))

    print('Zipping pack')
    shutil.make_archive('%s_Flushed' % zip_dest, 'zip', zip_dest)

    print('Cleaning')
    shutil.rmtree(zip_dest)

    print('Done!')

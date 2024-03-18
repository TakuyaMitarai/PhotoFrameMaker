from PIL import Image
import os

def add_frame_to_image(image_path, output_path):
    with Image.open(image_path) as img:
        exif_data = img.info.get('exif')
        width, height = img.size
        aspect_ratio = width / height

        # 3:2の横写真
        if 1.5 * 0.95 <= aspect_ratio <= 1.5 * 1.05:
            frame_thickness = width // 50
            white_frame_thickness = width // 1000
            outer_frame_size = (width + 2 * (frame_thickness + white_frame_thickness), height + 2 * (frame_thickness + white_frame_thickness))
            img_with_frame = Image.new('RGB', outer_frame_size, 'white')
            inner_frame_start = (frame_thickness, frame_thickness)
            img_with_frame.paste(Image.new('RGB', (outer_frame_size[0] - 2 * frame_thickness, outer_frame_size[1] - 2 * frame_thickness), 'black'), inner_frame_start)
            img_start = (frame_thickness + white_frame_thickness, frame_thickness + white_frame_thickness)
            img_with_frame.paste(img, img_start)

        # 2:3の縦写真
        elif 2 / 3 * 0.95 <= aspect_ratio <= 2 / 3 * 1.05:
            new_width = int(height * 4 / 5)
            img_with_frame = Image.new('RGB', (new_width, height), 'black')
            img_with_frame.paste(img, (int((new_width - width)/2), 0))

        # 16:9の横写真
        elif 16 / 9 * 0.95 <= aspect_ratio <= 16 / 9 * 1.05:
            new_height = int(width * 2 / 3)
            img_with_frame = Image.new('RGB', (width, new_height), 'black')
            img_with_frame.paste(img, (0, int((new_height - height) / 2)))

        else:
            # アスペクト比がどれにも当てはまらない場合、元の画像をそのまま使用
            img_with_frame = img.copy()
        
        if exif_data:
            img_with_frame.save(output_path, exif=exif_data, quality=100)
        else:
            img_with_frame.save(output_path, quality=100)

def process_images():
    input_dir = 'original'
    output_dir = 'processing'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            add_frame_to_image(input_path, output_path)

process_images()

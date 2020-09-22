import moderngl

from PIL import Image

from renderer.renderunit import RenderUnit

class ImageTextureRenderUnit(RenderUnit):
    def __init__(self, 
                context, 
                path, 
                flip_x = False, 
                flip_y = True, 
                mipmap = False,
                mipmap_levels=(),
                anisotropy=1.0):
        RenderUnit.__init__(self)

        with Image.open(path) as image:

            if image.is_animated:
                image = self.to_animated_image(image)
            
            if flip_x:
                image = image.transpose(Image.FLIP_LEFT_RIGHT)

            if flip_y:
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
                

            if image.palette and image.palette.mode.lower() in ["rgb", "rgba"]:
                mode = image.palette.mode
                image = image.convert(mode)

            data = image.tobytes()
            components = len(data) // (image.size[0] * image.size[1])

            self.texture = context.texture(image.size, components, data)

            if mipmap_levels:
                mipmap = True

            if mipmap:
                self.texture.build_mipmaps(*mipmap_levels)
                if anisotropy:
                    self.texture.anisotropy = anisotropy

    def to_animated_image(self, image):
            anim = Image.new(
                image.palette.mode,
                (image.width, image.height * image.n_frames),
            )
            anim.putalpha(0)

            for frame_number in range(image.n_frames):
                image.seek(frame_number)
                frame = self._palette_to_raw(image, mode="RGBA")
                anim.paste(frame, (0, frame_number * image.height))

            return anim
        
    def render_unit(self):
        return self.texture
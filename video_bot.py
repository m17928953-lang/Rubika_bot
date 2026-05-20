from rubpy.bot import BotClient, filters
import os
import cv2
import tempfile

# بعداً توکن رو توی Render تنظیم می‌کنیم
BOT_TOKEN = os.environ.get("BEAACI0FXHCWELEBFSBHTBEWDTYGEXMNSQRTCFFOYXTWRUMYQCXRJDPDTSJRIALW")

def convert_to_circle(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    size = min(width, height)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (480, 480))
    
    frame_count = 0
    max_frames = fps * 60
    
    while True:
        ret, frame = cap.read()
        if not ret or frame_count >= max_frames:
            break
        
        start_x = (width - size) // 2
        start_y = (height - size) // 2
        cropped = frame[start_y:start_y+size, start_x:start_x+size]
        resized = cv2.resize(cropped, (480, 480))
        out.write(resized)
        frame_count += 1
    
    cap.release()
    out.release()
    return output_path

app = BotClient(BOT_TOKEN)

@app.on_update(filters.video)
async def handle_video(client, update):
    message = update.new_message
    print("ویدیو دریافت شد! در حال پردازش...")
    
    try:
        video_file = await message.download()
        output_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
        convert_to_circle(video_file, output_path)
        await message.reply_video_note(video_note=output_path)
        print("ویدیو مسیج ارسال شد!")
        os.remove(video_file)
        os.remove(output_path)
    except Exception as e:
        print(f"خطا: {e}")

if __name__ == "__main__":
    print("ربات روشن شد!")
    app.run()
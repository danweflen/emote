#Preprocess data sets to without the tensorflow dependency on Discovery.
import cv2
import sys, os
import argparse
from gui.video import FrameWriter
from util import paths
from face_process import detect_and_align_face



def main():

    #Parse command args
    parser = argparse.ArgumentParser(description='Emote - Preprocess: A utility to detect faces in video or images without installing tensorflow')
    parser.add_argument('command', type=str, help='Subcommand to be run')

    args = parser.parse_args(sys.argv[1:2])

    if args.command is None:
        print_help()
    elif args.command == 'image':
        image(sys.argv[2:])
    elif args.command == 'video':
        video(sys.argv[2:])
    elif args.command == 'mirror':
        mirror(sys.argv[2:])
    else:
        print_help()
        quit(1)

def image(options):

    parser = argparse.ArgumentParser(description='Image Face detection')
    parser.add_argument('input_file', type=str, help='Image to be processed')
    parser.add_argument('output_file', type=str, help='Output file')
    parser.add_argument('image_size', type=int, help='Output image size')
    parser.add_argument('-g', action='store_true', default=False, help='Output image in grayscale (default if False)')

    args = parser.parse_args(options)

    path = args.input_file
    pic = cv2.imread(path)
    face = detect_and_align_face(pic, args.image_size, args.g)

    cv2.imwrite(args.output_file, face)
    print("Finshed ")

def video(options):
    parser = argparse.ArgumentParser(description='Video face detection')
    parser.add_argument('input_file', type=str, help='Image to be processed')
    parser.add_argument('output_dir', type=str, help='Output directory')
    parser.add_argument('image_size', type=int, help='Size of output image')
    parser.add_argument('-g', action='store_true', default=False, help='Output image in grayscale (default if False)')

    args = parser.parse_args(options)

    writer = FrameWriter(args.output_dir, args.input_file)
    cap = cv2.VideoCapture(args.input_file)
    _detect_faces_from_video(cap, writer, args.image_size, grayscale=args.g)

def mirror(options):
    parser = argparse.ArgumentParser(description='Mirrors videos over the y-axis')
    parser.add_argument('input_file', type=str, help='Video to be processed')
    parser.add_argument('output_dir', type=str, help='Output directory')
    parser.add_argument('image_size', type=int, help='Size of output image')
    parser.add_argument('-g', action='store_true', default=False, help='Output image in grayscale (default if False)')

    args = parser.parse_args(options)

    basename = os.path.basename(args.input_file)
    basename = 'Mirror' + basename
    writer = FrameWriter(args.output_dir, os.path.dirname(args.input_file) + '/' + basename)
    cap = cv2.VideoCapture(args.input_file)
    _detect_faces_from_video(cap, writer, args.image_size, mirror=True, grayscale=args.g)


def _detect_faces_from_video(cap, writer, image_size, mirror=False, grayscale=False):

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret:
            alignedFace = detect_and_align_face(frame, image_size, grayscale=grayscale)
            if alignedFace is not None:
                if mirror:
                    alignedFace = cv2.flip(alignedFace, 1)
                writer.write(alignedFace)
        else:
            break

    # When everything done, release the capture
    cap.release()


def print_help():
    print("preprocess [--help] <command>")
    print("")
    print("Subcommands:")
    print("image        Source is an image file")
    print("video        Source is a video file")
    print("mirror       Mirror the source video")

    print("Use the --help option on any subcommand for option")
    print("information relating to that command")

if __name__ == "__main__":
    main()

import cv
import cv2

def hs_histogram(src):
    # Convert to HSV
    hsv = cv.CreateImage(cv.GetSize(src), 8, 3)
    cv.CvtColor(src, hsv, cv.CV_BGR2HSV)

    # Extract the H and S planes
    h_plane = cv.CreateMat(src.rows, src.cols, cv.CV_8UC1)
    s_plane = cv.CreateMat(src.rows, src.cols, cv.CV_8UC1)
    cv.Split(hsv, h_plane, s_plane, None, None)
    planes = [h_plane, s_plane]

    h_bins = 20
    s_bins = 8
    hist_size = [h_bins, s_bins]
    # hue varies from 0 (~0 deg red) to 180 (~360 deg red again */
    h_ranges = [0, 180]
    # saturation varies from 0 (black-gray-white) to
    # 255 (pure spectrum color)
    s_ranges = [0, 255]
    ranges = [h_ranges, s_ranges]
    scale = 10
    hist = cv.CreateHist([h_bins, s_bins], cv.CV_HIST_ARRAY, ranges, 1)
    cv.CalcHist([cv.GetImage(i) for i in planes], hist)
    (_, max_value, _, _) = cv.GetMinMaxHistValue(hist)

    height = 240;
    width=  (h_bins*s_bins*6);
    hist_img = cv.CreateImage((width,height), 8, 3)
    hsv_color = cv.CreateImage((1,1),8,3)
    rgb_color = cv.CreateImage((1,1),8,3)
    bin_w = width / (h_bins * s_bins);
    for h in range(h_bins):
        for s in range(s_bins):
            bin_val = cv.QueryHistValue_2D(hist,h,s)
            i = h*s_bins+s
            intensity = cv.Round(bin_val * height / max_value)
            cv.Set2D(hsv_color,0,0,cv.Scalar(h*180.0 / h_bins,s*255.0/s_bins,230,0));
            cv.CvtColor(hsv_color,rgb_color,cv.CV_HSV2BGR);
            color = cv.Get2D(rgb_color,0,0);
            cv.Rectangle(hist_img,
                         (i*bin_w, height),
                         ((i+1)*bin_w ,height-intensity),
                         color, -1,8,0)
    return hist_img

if __name__ == '__main__':
    src = cv2.imread("d:\\T2l1N7XbNXXXXXXXXX_!!752473764.jpg_310x310.jpg")
    corpImg = cv2.getRectSubPix(src,(150,150),(155,155))
    cv.NamedWindow("Source", 1)
    cv2.imshow("Source", corpImg)

    cv.NamedWindow("H-S Histogram", 1)
    cv.ShowImage("H-S Histogram", hs_histogram(cv.fromarray(corpImg)))

    cv.WaitKey(0)
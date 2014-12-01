#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <gdiplus.h>
DWORD WINAPI ThreadFunc(void* data);
int lastSize = 0;

int main()
{
    SOCKET s = newsock();
    LPCTSTR tstfile = L"test";;
    struct GdiplusStartupInput gdiplusStartupInput = {1,NULL,FALSE,FALSE};
    ULONG_PTR gdiplusToken;
    GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);
    HANDLE thread = CreateThread(NULL, 0, ThreadFunc, NULL, 0, NULL);
    for(int i=0;i<10000;i++)
    {
    HDC hdc = GetDC(NULL);
    HDC hDest = CreateCompatibleDC(hdc);
    int height = GetSystemMetrics(SM_CYVIRTUALSCREEN);
    int width = GetSystemMetrics(SM_CXVIRTUALSCREEN);
    HBITMAP hbDesktop = CreateCompatibleBitmap( hdc, width, height);
    SelectObject(hDest, hbDesktop);
    BitBlt(hDest, 0,0, width, height, hdc, 0, 0, SRCCOPY);
    ReleaseDC(NULL, hdc);
    DeleteDC(hDest);
    SaveJpeg(hbDesktop,tstfile,30);
    sendFile(s);
    DeleteObject(hbDesktop);
    DeleteDC(hdc);
    //Sleep(200);
    }
    GdiplusShutdown(gdiplusToken);
    return 0;
}

void sendFile(SOCKET s)
{
        FILE *file;
        file = fopen("test", "rb");
        int size;
        fseek(file, 0, SEEK_END);
        size = ftell(file);
        fseek(file, 0, SEEK_SET);
        if(size!=lastSize)
            {
                lastSize = size;
                int bytes_read;
                char *mtu[size];
                bytes_read = fread(mtu,1,size, file);
                send_prefix(bytes_read,s);
                send(s,mtu,bytes_read,0);
            }
        fclose(file);
}



int send_prefix(int num, SOCKET s)
{
    send(s, (const char*)(&num), sizeof(unsigned long), 0);
}


void SaveJpeg(HBITMAP hBmp, LPCWSTR lpszFilename, ULONG uQuality)
{
    GpBitmap* pBitmap;
    GdipCreateBitmapFromHBITMAP(hBmp, NULL, &pBitmap);
    CLSID imageCLSID;
    GetEncoderClsid(L"image/jpeg", &imageCLSID);;
    EncoderParameters encoderParams;
    encoderParams.Count = 1;
    encoderParams.Parameter[0].NumberOfValues = 1;
    encoderParams.Parameter[0].Guid  = EncoderQuality;
    encoderParams.Parameter[0].Type  = EncoderParameterValueTypeLong;
    encoderParams.Parameter[0].Value = &uQuality;
    GdipSaveImageToFile(pBitmap, lpszFilename, &imageCLSID, &encoderParams);
    GdipDisposeImage(pBitmap);
    DeleteObject(pBitmap);
    DeleteObject(hBmp);
}

int GetEncoderClsid(const WCHAR* format, CLSID* pClsid)
{
   UINT  num = 0;          // number of image encoders
   UINT  size = 0;         // size of the image encoder array in bytes

   ImageCodecInfo* pImageCodecInfo = NULL;
   GetImageEncodersSize(&num, &size);;
   if(size == 0)

      return -1;  // Failure
   pImageCodecInfo = (ImageCodecInfo*)(malloc(size));
   if(pImageCodecInfo == NULL)
      return -1;  // Failure
   GetImageEncoders(num, size, pImageCodecInfo);
    UINT j;
   for(j = 0; j < num; ++j)
   {
      if( wcscmp(pImageCodecInfo[j].MimeType, format) == 0 )
      {
         *pClsid = pImageCodecInfo[j].Clsid;
         free(pImageCodecInfo);
         return j;  // Success
      }
   }
   free(pImageCodecInfo);
   return -1;  // Failure
}

DWORD WINAPI ThreadFunc(void* data) {
  // Do stuff.  This will be the first function called on the new thread.
  // When this function returns, the thread goes away.  See MSDN for more details.
  SOCKET r = newsock();

//s  send(s, (const char*)(&num), sizeof(unsigned long), 0);
  char *buff[4];

  while(1){
        recv(r,buff,sizeof(buff),0);
        printf("buffer is full!");
  }
}

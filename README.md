# CBC/Radio-Canada C2PA Dash Demo

## requirements
docker
python3
pyinstaller
c2patool
aws key configuration

## Run
```sh
docker compose up
```
http://localhost:81/

## instructions

## 1. Certificates
### a. Use a self-signed certificate 
Nothing to do, we'll clone a test one with c2patool

### b. Build a signer
```sh

#Update key information in the signer
pyinstaller --onefile signer.py

#test the signer
echo "votre_message" | ./dist/test

# copy your ps256.pub file in asset/sample/
```

## 2. Encode the mp4 into a Dash fmp4
```sh
cd asset
cp -r ../dist .
wget https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4
MP4Box Big_Buck_Bunny_360_10s_1MB.mp4 -dash 4000 -frag 40000 -rap -profile live -out c2pa_dash_demo/output.mpd  # fragment are smaller than 4096 for the kms signer
```

# 3 Sign the fmp4 either with the self signed certificate or the AWS KMS service
```sh
wget https://github.com/contentauth/c2patool/releases/download/v0.9.12/c2patool-v0.9.12-universal-apple-darwin.zip
unzip c2patool-v0.9.12-universal-apple-darwin.zip -d c2pa_cli
cp c2pa_cli/c2patool/c2patool .
```

# with the signer
Go into sample/test.json and replace sign_cert with your own public key:
"sign_cert": "!!! REPLACE BY YOUR OWN PUBLIC KEY !!!",
```sh
c2patool -m sample/test.json --signer-path dist/test -o dash-signed/ "c2pa_dash_demo/Big_Buck_Bunny_360_10s_1MB_dashinit.mp4" fragment --fragments_glob "Big_Buck_Bunny_360_10s_1MB_dash*[0-9].m4s"
```

### Without the signer
```sh
c2patool -m c2pa_cli/c2patool/sample/test.json -o c2pa_dash_demo_signed/ "c2pa_dash_demo/Big_Buck_Bunny_360_10s_1MB_dashinit.mp4" fragment --fragments_glob "Big_Buck_Bunny_360_10s_1MB_dash*[0-9].m4s"
```

# 4 Copy the playlist back into the signed asset
```sh
cp c2pa_dash_demo/output.mpd c2pa_dash_demo_signed/c2pa_dash_demo
```

# 5 Copy the asset in the website
```sh
cp -r c2pa_dash_demo_signed/c2pa_dash_demo ../html/
```


## Credits
* https://dashif.org/events/special-sessions/ [June 7, 2024: DASH-IF Special Session: Content Authenticity and Provenance in DASH]
* https://github.com/contentauth/c2patool/blob/main/src/callback_signer.rs
* https://github.com/aws-solutions-library-samples/guidance-for-media-provenance-with-c2pa-on-aws




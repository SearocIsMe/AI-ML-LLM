

## MountVolume.SetUp failed for volume "istio-token" : failed to fetch token: the server could not find the requested resource
``` 
remove below from deployment
      {
        "name": "istio-token",
        "projected": {
          "sources": [
            {
              "serviceAccountToken": {
                "audience": "istio-ca",
                "expirationSeconds": 43200,
                "path": "istio-token"
              }
            }
          ],
          "defaultMode": 420
        }
      },
```
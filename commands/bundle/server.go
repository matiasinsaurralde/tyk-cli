package bundle

import (
	"net/http"

	logrus "github.com/Sirupsen/logrus"
	"github.com/TykTechnologies/tyk-cli/server"
)

func BundleServer(upstreamURL string, listenAddress string) (err error) {
	manifest, err := loadManifest()
	if err != nil {
		return err
	}
	logrus.Info("Starting bundle server")
	s, err := server.NewServer(upstreamURL, manifest)
	if err != nil {
		return err
	}
	http.ListenAndServe(listenAddress, s.Handler)
	return err
}

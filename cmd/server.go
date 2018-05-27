package cmd

import (
	"fmt"

	"github.com/TykTechnologies/tyk-cli/commands/bundle"
	"github.com/spf13/cobra"
)

const (
	defaultUpstreamURL   = "http://httpbin.org"
	defaultListenAddress = "127.0.0.1"
	defaultListenPort    = 8080
)

var (
	upstreamURL   string
	listenAddress string
	listenPort    int
)

var serverCmd = &cobra.Command{
	Use:   "server",
	Short: "Start a HTTP server for middleware testing",
	Long:  `This command starts a HTTP server for middleware testing.`,
	Run: func(cmd *cobra.Command, args []string) {
		listen := fmt.Sprintf("%s:%d", listenAddress, listenPort)
		err := bundle.BundleServer(upstreamURL, listen)
		if err != nil {
			fmt.Println("Error: ", err)
		}
	},
}

func init() {
	bundleCmd.AddCommand(serverCmd)
	serverCmd.PersistentFlags().StringVarP(&upstreamURL, "upstream", "u", defaultUpstreamURL, "Upstream URL")
	serverCmd.PersistentFlags().StringVarP(&listenAddress, "listen", "l", defaultListenAddress, "Listen address")
	serverCmd.PersistentFlags().IntVarP(&listenPort, "port", "p", defaultListenPort, "Listen port")
}

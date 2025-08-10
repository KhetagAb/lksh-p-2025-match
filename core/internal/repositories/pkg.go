package repositories

import (
	"embed"
	"path"
)

var queriesFS embed.FS

func GetQuery(table, action string) (*string, error) {
	queryPath := path.Join("query", table, action+".sql")
	query, err := queriesFS.ReadFile(queryPath)
	if err != nil {
		return nil, err
	}
	out := string(query)
	return &out, nil
}

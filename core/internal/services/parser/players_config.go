package parser

import (
	"match/internal/configs"
	"strings"
)

type ConfigPlayerParser struct {
	cfg *configs.Users

	tgUsernameToName map[string]string
}

func (c *ConfigPlayerParser) GetTgUsernameToName() map[string]string {
	if c.tgUsernameToName != nil {
		return c.tgUsernameToName
	}

	tgUsernameToName := make(map[string]string)
	for _, user := range c.cfg.Users {
		userParts := strings.Split(user, ":")
		tgUsernameToName[strings.TrimSpace(userParts[0])] = strings.TrimSpace(userParts[1])
	}
	c.tgUsernameToName = tgUsernameToName
	return tgUsernameToName
}

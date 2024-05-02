package app

import (
	"strings"
)

func validatePixivTag(tag *string) (valid bool, pageNum string) {
	// split by ";" and get the last element, 
	// for the other elements, just join them back with ";"
	splitTag := strings.Split(*tag, ";")
	if len(splitTag) == 0 {
		return len(*tag) > 0, ""
	}

	pageNum = splitTag[len(splitTag)-1]
	*tag = strings.Join(splitTag[:len(splitTag)-1], ";")
	if len(*tag) == 0 {
		return false, ""
	}

	return true, pageNum
}

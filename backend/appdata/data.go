package appdata

import (
	"reflect"

	"github.com/KJHJason/Cultured-Downloader-Logic/logger"
)

func checkIfValueIsSame(oldValue, newValue interface{}) bool {
	newValueKind := reflect.TypeOf(newValue).Kind()
	oldValueKind := reflect.TypeOf(oldValue).Kind()
	if newValueKind == reflect.Slice {
		if oldValueKind != reflect.Slice {
			return false
		}

		newVal := reflect.ValueOf(newValue)
		oldVal := reflect.ValueOf(oldValue)
		if newVal.Len() != oldVal.Len() {
			return false
		}

		for i := 0; i < newVal.Len(); i++ {
			if newVal.Index(i).Interface() != oldVal.Index(i).Interface() {
				return false
			}
		}
		return true
	}
	return oldValue == newValue
}

// Mainly used for validating the data loaded from file to its correct type and removing unsupported data
func convertDataMapInterface(values map[string]interface{}) {
	for k, v := range values {
		items, isSliceInterface := v.([]interface{})
		if !isSliceInterface {
			switch t := v.(type) {
			case bool:
				values[k] = t
			case float64:
				values[k] = t
			case int:
				values[k] = t
			case string:
				values[k] = t
			default:
				logger.MainLogger.Errorf(
					"Unsupported data type for key %q with type \"%T\", this key will be removed.", k, v)
				delete(values, k) // Remove invalid data
			}
			continue
		}

		if len(items) == 0 {
			continue
		}

		// Take the first element and check its type
		firstElement := items[0]
		switch firstElement.(type) {
		case bool:
			bools := make([]bool, len(items))
			for i, item := range items {
				bools[i] = item.(bool)
			}
			values[k] = bools
		case float64:
			floats := make([]float64, len(items))
			for i, item := range items {
				floats[i] = item.(float64)
			}
			values[k] = floats
		case int:
			ints := make([]int, len(items))
			for i, item := range items {
				ints[i] = item.(int)
			}
			values[k] = ints
		case string:
			strings := make([]string, len(items))
			for i, item := range items {
				strings[i] = item.(string)
			}
			values[k] = strings
		default:
			logger.MainLogger.Errorf(
				"Unsupported data type for key %q with slice of type \"%T\", this key will be removed.", k, firstElement)
			delete(values, k) // Remove invalid data
		}
	}
}

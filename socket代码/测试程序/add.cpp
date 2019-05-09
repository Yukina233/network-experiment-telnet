#include <stdio.h>

int main(int argc, char *argv[ ])
{
	int buf;
	int sum = 0;
	int i = 0;
	
	if (argc == 1) {
		int n;
		scanf("%d", &n);
		for (i = 0; i < n; i++) {
			scanf("%d", &buf);
			sum += buf;
		}
	}
	else {
		for (i = 1; i < argc; i++) {
			sscanf(argv[i], "%d", &buf);
			sum += buf;
		}
	}
	printf("%d\n", sum);
	return 0;
}
import { Column } from '../entities/column';
import { GridOptionsService } from '../gridOptionsService';
export declare const iconNameClassMap: {
    [key: string]: string;
};
/**
 * If icon provided, use this (either a string, or a function callback).
 * if not, then use the default icon from the theme
 * @param {string} iconName
 * @param {GridOptionsService} gridOptionsService
 * @param {Column | null} [column]
 * @returns {HTMLElement}
 */
export declare function createIcon(iconName: string, gridOptionsService: GridOptionsService, column: Column | null): HTMLElement;
export declare function createIconNoSpan(iconName: string, gridOptionsService: GridOptionsService, column?: Column | null, forceCreate?: boolean): HTMLElement | undefined;
